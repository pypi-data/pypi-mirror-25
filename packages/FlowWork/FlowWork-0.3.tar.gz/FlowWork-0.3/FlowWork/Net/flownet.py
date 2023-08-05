# -*- coding:utf-8 -*-
from selenium.webdriver.common.proxy import *
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from qlib.log import show
from bs4 import BeautifulSoup as BS
from bs4.element import NavigableString, Tag
from hashlib import md5
import os, socket, time
import logging , re
import configparser

logging.basicConfig(level=logging.INFO)


phantomjs_path = os.popen("which phantomjs").read().strip()
if not phantomjs_path:
    show("install phantomjs first!!")
    sys.exit(1)


SocialKit_cache_max_size = '1000468'
storage_path = '/tmp/'
cookies_path = '/tmp/cookie.txt'

class ProxyNotConnectError(Exception):
    pass


def test_proxy(proxy):
    t,s,p = proxy.split(":")
    s = s[2:]
    p = int(p)
    try:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((s,p))
    except Exception as e:
        show(e)
        return False
    return True



class FLowNet:
    keys = Keys
    def __init__(self, url=None, proxy=False, load_img=False, random_agent=False,agent=None,**options):
        
        if proxy:
            if not test_proxy(proxy):
                raise ProxyNotConnectError(proxy + " not connected")

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        if agent:
            dcap["phantomjs.page.settings.userAgent"] = agent

        # dcap['phantomjs.page.settings.resourceTimeout'] = '5000'
        load_image = 'true' if load_img else 'false' 
        timeout = options.get('timeout')

        web_service_args = [
            '--load-images=' + load_image,
        ]

        if proxy:
            proxy_t, proxy_c = proxy.split("//")
            proxy_t = proxy_t[:-1]
            show(proxy_c, proxy_t)
            web_service_args += [
                '--proxy=' + proxy_c,
                '--proxy-type=' + proxy_t,
                '--local-storage-path=' + storage_path,
                '--cookies-file=' + cookies_path,
                '--local-storage-quota=' + str(SocialKit_cache_max_size),
            ]

        self.phantom = webdriver.PhantomJS(phantomjs_path,service_args=web_service_args, desired_capabilities=dcap)
        if timeout:
            self.phantom.set_page_load_timeout(int(timeout))
        self.dcap = dcap
        self.datas = []
        self.render_text = {}
        if url:
            self.go(url)

    def extract_S(self, loc):
        id_i = loc.find("#")
        class_i = loc.find(".")

        if id_i < class_i:
            tag = loc[:id_i].lower()
            id_s = loc[id_i:class_i]
            class_s = loc[class_i:]

        else:
            tag = loc[:class_i].lower()
            class_s = loc[class_i:id_i]
            id_s = loc[id_i:]

        return tag, class_s, id_s

    def flow(self,loc, ac, cursor, screenshot=True, submit=False, **kargs):
        """
        exm:
            #main/C
            .in/I'hello,work\n',.in-2/I'if no .in this will be flow'->[cond2]
            .over/C
            [cond2]#rechck/I'hello,work'



            action : I = input / C = click / D = clear / M = move scroll
        """
        if_screenshot = screenshot
        text = None
        
        if '->' in ac:
            ac, cursor =  ac.split("->")
        else:
            cursor += 1

        if '{' in ac and '}' in ac:
            key = re.findall(r'\{(.+?)\}', ac)[0]
            if key in self.render_text:
                ac = ac.format(*{key: self.render_text[key]})
            else:
                show("no found key:", key , " in render", color='red', log=True, k='error')

        if '[' in loc and ']' in loc:
            text = re.findall(r'\[(.+?)\]', loc)[0]
            loc = re.sub(r'\[(.+?)\]', '', loc)
            show('find text:',text)

        # show(cursor, loc, ac)
        if ac[0] == 'C':
            show('click:', loc, text)
            self.do(loc, text=text, **kargs)
            
        elif ac[0] == 'I':
            msg = re.findall(r'\'([\w\W]+)\'', ac)
            show('type:', msg, 'in',loc, text)
            self.do(loc, msg,text=text, **kargs)
            if submit:
                self.do(loc, '\n',text=text, **kargs)
            # self.do(loc, text=text, **kargs)
        elif ac[0] == 'D':
            show('clear:', loc, text)
            self.do(loc, clear=True, **kargs)
        elif ac[0] == 'M':
            pass

        if if_screenshot:
            show("screen:", cursor)
            self.screenshot(str(cursor))

        return cursor

        
    def parse_render_text(self, f):
        with open(f) as fp:
            for l in fp:
                k,v = l.split(":", maxsplit=1)
                self.render_text[k] = v



    def flow_doc(self, f, render_text=None, timeout=7):
        """
        exm:
            #main/C
            .in/I'hello,work\n',.in-2/I'if no .in this will be flow'->[cond2]
            .over/C
            [cond2]#rechck/I'hello,work'
        """
        if render_text:
            self.parse_render_text(render_text)

        if os.path.exists(f):
            flows = [i.strip() for i in open(f).readlines()]
            
        elif isinstance(f, list):
            flows = f
        else:
            flows = f.split('\n')
        
        cursor = 0
        wait = 0
        
        while 1:
            if_submit = False
            if cursor >= len(flows):
                break
            pre_order = flows[cursor]

            # 结束标志
            if pre_order == '[over]':
                break

            #  submit flag
            if "I'" in pre_order:
                if cursor + 1 < len(flows):
                    if "I'" in flows[cursor+1]:
                        if_submit = False
                    else:
                        if_submit = True


            # [正则匹配标志] 为最短路径选取
            if '[' in pre_order:
                wait = timeout

            # 强置等待时间
            if pre_order[0] in '0123456789' and pre_order[-1] in '0123456789':
                show("wait :", pre_order)
                self._wait(int(pre_order))
                cursor += 1
                continue

            if pre_order.startswith("http"):
                show("--> ", pre_order)
                self.go(pre_order) 
                cursor += 1
                continue
            show(cursor, pre_order)
            if ',' in pre_order:
                conditions = pre_order.split(",")
                for i in conditions:
                   loc, ac =  i.split("/")
                   loc = loc.strip()
                   ac = ac.strip()
                   cursor =  self.flow(loc, ac, cursor, wait=wait, submit=if_submit)
            else:
                loc, ac =  pre_order.split("/")
                loc = loc.strip()
                ac = ac.strip()
                cursor =  self.flow(loc, ac, cursor,wait=wait, submit=if_submit)




    def go(self, url):
        self.phantom.get(url)
        self.soup = BS(self.phantom.page_source, 'lxml')

    def _wait(self, selector, timeout=7):
        if isinstance(selector, int):
            time.sleep(selector)
        return None

        if '[' in selector:
            selector = selector[:selector.find('[')]
        try:
            if '.' in selector:
                wait = WebDriverWait(self.phantom,timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME,selector[1:])))
            elif '#' in selector:
                wait = WebDriverWait(self.phantom,timeout).until(
                    EC.presence_of_element_located((By.ID,selector[1:])))
            else:
                wait = WebDriverWait(self.phantom,timeout).until(
                    EC.presence_of_element_located((By.TAG_NAME,selector)))
        except Exception as e:
            self.screenshot('debug')
            raise e

    def save_tmp(self, key=None):
        if self.phantom.current_url in self.datas:
            self.datas[self.phantom.current_url].append(self.phantom.page_source)
        else:
            self.datas[self.phantom.current_url] = [self.phantom.page_source]

    def screenshot(self, *names):
        if len(names) > 0:
            self.phantom.get_screenshot_as_file('/tmp/' + names[0]+".png")
        else:
            self.phantom.get_screenshot_as_file('/tmp/one.png')

    def do(self, selectID, *args, text=None,save_screen=True,save_data=False, wait=None, clear=False, callback=None,**kargs):
        """
        css select mode :
            div .
        """
        # before_hash = md5(self.phantom.page_source.encode("utf8")).hexdigest()
        if save_screen:
            self.screenshot()
        selectID = selectID.strip()
        if '>' in selectID:
            self._wait(selectID.split(">")[-1])
        else:
            self._wait(selectID)
        res = None

        if text:
            target = self.back_recur_find(selectID, text)
            if not target:
                self._wait(1)
                for i in range(5):
                    show("try ", i,"time...")
                    if save_screen:
                        self.screenshot()
                    self._wait(wait)
                    target = self.back_recur_find(selectID, text)
                    if target:
                        break

            if not target:
                raise NoSuchElementException()

        else:
            target = self.find(selectID)

        if not target:
            show("Not found :", selectID, color='yellow', log=True, k='warn')
            return self

        if clear:
            show("clear :",selectID, log=True, k='debug')
            target.clear()

        if len(args) == 1:   
            target.send_keys(args[0])

        elif len(args) == 0:
            if target.tag_name == 'a' and 'javascript' not in target.get_attribute("href"):
                show("directly go -> ",target.get_attribute("href"))
                self.go(target.get_attribute("href"))

            else:
                show("click: ",target.get_attribute("href"))
                target.click()
        else:
            raise Exception("no such operator!!")


        if wait:
            if isinstance(wait, str):
                self._wait(wait)
            elif isinstance(wait, int):
                time.sleep(wait)
            else:
                show("unknow wait type: (only: int, str)", color='red')

        if callback:
            callback(self.phantom.page_source)

        if save_data:
            if isinstance(save_data, bool):
                self.save_tmp()
            elif isinstance(save_data, str):
                # a fliter ...
                pass
        if save_screen:
            self.screenshot()

        # af_hash = md5(self.phantom.page_source.encode("utf8")).hexdigest()
        # if af_hash == before_hash:
            # show("no response")
            # try:
                # href = target.get_attribute("href")
                # show("try directly go ...")
                # self.go(href)
            # except Exception as e:
                # pass

        return self

    def _get_absolute_path(self, ele):
        f = ele.name
        if 'id' in ele.attrs:
            f += '#'+ele.attrs['id']
        elif 'class' in ele.attrs:
            f += '#'+ ele.attrs['class']

        while 1:
            if ele.parent.name in  ('body', 'html'):
                break
            ele = ele.parent

            tmp = ele.name
            if 'id' in ele.attrs:
                tmp += '#' + ele.attrs['id']
            elif 'class' in ele.attrs:
                tmp += '#' + ele.attrs['class'][0]
            f = tmp + ">" + f

        return f


    def search(self, css_select, key_text, parser='lxml'):
        b = BS(self.html(), 'lxml')
        for module in b.find_all(text=re.compile(key_text)):
            path = self._get_absolute_path(module.parent)
            if css_select in path:
                return path

    def back_tree(self, t, key, coefficient=0):
        
        if t.find(text=re.compile('(' + key + ')')):
            return t,coefficient
        else:
            coefficient += 1
            if t.parent:
                return self.back_tree(t.parent, key, coefficient)
            else:
                return None, 9999

    def back_inclu(self, t, css):
        r = t.find(css)
        if r:
            return r
        else:
            if t.parent:
                return self.back_inclu(t.parent, css)
            else:
                return None

    def back_recur_find(self, css, key):
        targets = self.phantom.find_elements_by_css_selector(css)
        self.soup = BS(self.phantom.page_source, 'lxml')
        if len(targets) > 1:
            eles = self.soup(css)
            try:
                e = self.soup(text=re.compile(key))[0]
            except IndexError:
                return None
            may_e = self.back_inclu(e.parent, css)

            if not may_e:
                return None

            for i, p in enumerate(eles):
                if p == may_e:
                    try:
                        return targets[i]
                    except IndexError:
# this is condition when some element loaded but other is loading. this may cause 
# 'targets' is not same as 'eles'
                        return None
        else:
            try:
                return targets[0]
            except IndexError:
                return None



    def related_find(self, css_selector, key=''):
        targets = self.phantom.find_elements_by_css_selector(css_selector)
        self.soup = BS(self.phantom.page_source, 'lxml')
        if len(targets) > 1:
            eles = self.soup(css_selector)
            ele,max_relate_t = self.back_tree(eles[0], key)
            choise = 0
            for i,t in enumerate(eles):
                e,ts = self.back_tree(t, key)
                # show(ts, e.name)
                if ts < max_relate_t:
                    
                    choise = i
                    ele = e
                    max_relate_t = ts
            return targets[choise]

        else:
            return targets[0]

    def find(self, selectID, fuzzy=None):
        selectIDs = selectID.split(">")
        target = self.phantom
        targets = []
        l = len(selectIDs)
        for no, SLE in enumerate(selectIDs):
            try:
                if ':' in SLE:
                    n, i = SLE.split(':')
                    target = target.find_elements_by_css_selector(n)[int(i)]
                else:
                    target = target.find_element_by_css_selector(SLE)
                continue
            except NoSuchElementException as e:
                pass

            try:
                if SLE.startswith("."):
                    if ':' in SLE:
                        n, i = SLE[1:].split(':')
                        # show(n,i)
                        target = target.find_elements_by_class_name(n)[int(i)]
                    else:
                        target = target.find_element_by_class_name(SLE[1:])
                elif SLE.startswith("#"):
                    if ':' in SLE:
                        n, i = SLE[1:].split(':')
                        # show(n,i)
                        target = target.find_elements_by_id(n)[int(i)]
                    else:
                        target = target.find_element_by_id(SLE[1:])
                else:
                    if ':' in SLE:
                        n, i = SLE.split(':')
                        # show(n,i)
                        target = target.find_elements_by_tag_name(n)[int(i)]
                    else:
                        target = target.find_element_by_tag_name(SLE)
            except NoSuchElementException as e:
                show("can not found , continue", e)
                if no == l-1:
                    return 
                continue
        target.source = target.get_attribute('outerHTML')
        return target
    
    def html(self):
        return self.phantom.page_source


    def __call__(self, key, **kargs):
        return self.soup(key, **kargs)


# python3-
学习使用python，平时使用到的小代码

selenium库的使用

导入库

        from selenium import webdriver


Chrome

    1、获取webdriver对象

        driver=webdriver.Chrome()
        可以设置一些属性
        driver.maximize_window() #窗口最大化
        driver.set_window_size(375,667) #设置窗口大小
        driver.set_page_load_timeout(30) #设置页面超时时间
        添加cookie
        cookies=[{'domain': 'baidu.com', 'expiry': 1827812159, 'httpOnly': False, 'name': 'SINAGLOBAL', 'path': '/', 'secure': False, 'value': '4224864892411.2285.1512452159390'}, {'domain': 'baidu.com', 'expiry': 1558153604, 'httpOnly': False, 'name': 'UOR', 'path': '/', 'secure': False, 'value': ''}]
        #有些cookie浏览器无法识别，出现异常时直接pass即可
        ps 有时添加cookie失败是需要driver先打开网页，再添加cookie，然后刷新页面即可
        for cookie in cookies:
            try:
                driver.add_cookie(cookie_dict=cookie)
            except Exception as e:
                pass
        #删除cookie
        driver.delete_all_cookies()
        将本地Chrome的使用数据传入
        options=webdriver.ChromeOptions()
        options.add_argument("--user-data-dir="+r"C:\\Users\\mengxinhao\\appdata\\local\\Google\\Chrome\\User Data\\")
        不显示浏览器被自动化软件控制信息
        options.add_argument('disable-infobars')
        隐藏浏览器
        options.add_argument('headless')
        driver=webdriver.Chrome(chrome_options=options)

  
    2、打开一个网页

        driver.get("http://www.baidu.com")
  
    3、获取元素的方式

        driver.find_element_by_id("")#以元素id获取元素
        driver.find_element_by_class_name("")#以元素class属性获取元素
        driver.find_elements_by_tag_name("h1")#获取所有h1标签的元素
        driver.find_element_by_css_selector()
        driver.find_element_by_xpath()
        有时获取不到元素是因为元素在iframe里
        driver.switch_to_frame(driver.find_element_by_tag_name("iframe")) 
        或者使用
        driver.switch_to.frame()


    4、执行js

        js = 'window.scrollTo(0, document.body.scrollHeight);' #window.scrollTo(0,10000);
        driver.execute_script(js)

    5、截取页面

        driver.save_screenshot("sss.png")

    6、拖动元素

        from selenium.webdriver.common.action_chains import ActionChains
        source = driver.find_element_by_xpath("")
        ActionChains(driver).drag_and_drop_by_offset(source,300,0).perform()
        或
        # 可以控制拖动速度
        action = ActionChains(driver)
        action.click_and_hold(source).perform()
        for index in range(0,300):
            try:
                action.move_by_offset(index, 0).perform()  # 平行移动鼠标
            except UnexpectedAlertPresentException:
                break
            action.reset_actions()
            time.sleep(0.005)  # 等待停顿时间

    7、等待某个元素出现

        from selenium.webdriver.support.wait import WebDriverWait
        #每0.5秒检查一次iframe是否出现，5秒超时
        WebDriverWait(driver, 5, 0.5).until(lambda the_driver: the_driver.find_element_by_tag_name("iframe").is_displayed())

    8、获取网页信息

        driver.page_source

 PhantomJS
 
    1、PhantomJS浏览器没有界面，有时需要传入一些请求头
        添加请求头
        headers={
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Connection":"keep-alive",
            "Content-Type":"application/x-www-form-urlencoded",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
        }
        cap = DesiredCapabilities.PHANTOMJS.copy()#使用copy()防止修改原代码定义dict
        for key, value in headers.items():
           cap['phantomjs.page.customHeaders.{}'.format(key)] = value
        driver = webdriver.PhantomJS(desired_capabilities=cap)
        其他方法和chrome浏览器一样

    2、phantomjs截图是整个网页，chrome是浏览器显示的大小

Firfox

    1、获取webdriver对象
        from selenium.webdriver.firefox.options import Options
        #配置本地配置文件
        profile = webdriver.FirefoxProfile("C:\\Users\\mengxinhao\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xyzr60rp.default")
        options=Options()
        option.add_argument("-headless") #隐藏浏览器
        driver = webdriver.Firefox(firefox_profile=profile,firefox_options=options)

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import get_details as GD
import logging
import time
import os
from datetime import datetime


class Spotify_iOS:
    def __init__(self):
        self.welcome_screen = GD.Welcome_Container.pop('accessibility id')
        self.wc_screen_login = GD.WelcomeScreenLogin.pop('accessibility id')
        self.user_name_input = GD.Email_input.pop('accessibility id')
        self.password_input = GD.Password_input.pop('accessibility id')
        self.setting_icon = GD.Settings_icon.pop('xpath')
        self.login_button = GD.Login_after_input.pop('accessibility id')
        self.setting_profile = GD.Settings_profile.pop('accessibility id')
        self.log_out = GD.Log_out.pop('accessibility id')
        self.confirm_logout_btn = GD.Confirm_logout.pop('xpath')
        self.search_button = GD.Search_button.pop('accessibility id')
        self.header_button = GD.Header_button.pop('accessibility id')
        self.search_input = GD.Search_input.pop('accessibility id')
        self.header_play_button = GD.Header_Play_button.pop('accessibility id')
        self.pause_button = GD.Pause_button.pop('xpath')
        self.select_device = GD.Select_device.pop('xpath')
        self.close_pop_up = GD.Close_screen.pop('xpath')
        self.discon_device = GD.disconnect_device.pop('xpath')
        self.pl_bar = GD.Playing_bar.pop('accessibility id')
        self.previous_button = GD.Previous_Button.pop('accessibility id')
        self.next_button = GD.Next_Button.pop('accessibility id')
        self.slide_song = GD.slider_value.pop('accessibility id')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.x = Spotify_iOS.log_capture()
        self.file_handler = logging.FileHandler(self.x)
        self.file_handler.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(self.file_handler)
        self.driver = None
        model, version, id = Spotify_iOS.get_ios_details()
        try:
            self.desired_caps = {
                "platformName": "ios",
                "platformVersion": version,
                "deviceName": model,
                "automationName": "XCUITest",
                "bundleId": "com.spotify.client",
                "udid": id
            }
        except Exception as e:
            self.logger.critical(e)

    @staticmethod
    def get_ios_details():
        global user_id
        subprocess1 = subprocess.Popen("ios-deploy -c", shell=True, stdout=subprocess.PIPE)
        subprocess_return = subprocess1.stdout.read()
        str_data = subprocess_return.decode('utf-8')
        lst = str_data.split(',')
        iphone_model = lst[1].strip(' ')
        ios_version = lst[-2].strip(' ')
        get_userid = lst[0].split(' ')

        for i in get_userid:
            if len(i) > 18:
                user_id = i
        return iphone_model, ios_version, user_id

    @staticmethod
    def log_capture():
        DT = datetime.now()
        leaf_dir = '../Output/App_log'
        path2 = os.path.exists(leaf_dir)
        if not path2:
            print("App log directory created")
            os.makedirs(leaf_dir)
        else:
            pass
        log_file = os.path.join(leaf_dir, f'{DT.strftime("%d-%m-%y_%H-%M")}_device.log')
        return log_file

    def test_open_app(self):
        try:
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
            self.logger.debug('Opened Spotify App')
            time.sleep(2)
        except Exception as e:
            self.logger.critical(e)

    def test_click_on_settings_icon(self):
        time.sleep(5)
        setting_el = self.driver.find_element(AppiumBy.XPATH, self.setting_icon)
        setting_el.click()
        self.logger.debug('Clicked on Settings Icon')
        time.sleep(5)

    def test_verify_user(self):
        try:
            user_result = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.setting_profile)
            if user_result.text == self.setting_profile:
                self.logger.info(f'User is {self.setting_profile} as desired')
            return True
        except:
            scroll_el = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'About')
            wait_for_dev = WebDriverWait(self.driver, 2)
            self.driver.execute_script('mobile:scroll', {'element': scroll_el, "toVisible": True})
            fetch_button = wait_for_dev.until(EC.presence_of_element_located((
                AppiumBy.ACCESSIBILITY_ID, self.log_out)))
            fetch_button.click()
            confirm_logout_button = self.driver.find_element(AppiumBy.XPATH, self.confirm_logout_btn)
            confirm_logout_button.click()
            self.logger.debug(f'Logout is performed since it is not a Premium Account')
            return False

    def test_login_screen(self, user_name, pass_word):
        try:
            main_screen = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.welcome_screen)
            if main_screen.is_displayed():
                time.sleep(5)
                login_el = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.wc_screen_login)
                login_el.click()
                self.logger.info('Clicked on Welcome Login Screen')
                un_input = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.user_name_input)
                pw_input = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.password_input)
                un_input.send_keys(user_name)  # Dynamic Variables to be introduced
                self.logger.info("Entered the desired username ")
                time.sleep(1)
                pw_input.send_keys(pass_word)  # Dynamic Variables to be introduced
                self.logger.info("Password is being entered")
                time.sleep(1)
                login_el = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.login_button)
                login_el.click()
                self.logger.debug("Logging in with the given credentials")
                self.test_click_on_settings_icon()
                return True
        except:
            self.logger.debug('moving to click on settings icon function as App is already logged in with user')
            time.sleep(5)
            self.test_click_on_settings_icon()
            return False

    def test_select_song(self, kw_input):
        click_search_button = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.search_button)
        click_search_button.click()
        self.logger.debug('Selecting search button to search for keywords')
        click_header_button = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.header_button)
        click_header_button.click()
        send_data = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.search_input)
        send_data.send_keys(kw_input)
        self.logger.debug('Looking up for songs/playlist as per user input')
        ac = TouchAction(self.driver)
        # Below given co-ordinates might differ from phone to phone
        ac.tap(None, 116, 116, 1).perform()
        self.logger.debug('Selected on Playlists from the given input in searchbar')
        time.sleep(2)
        ac.tap(None, 101, 232, 1).perform()
        self.logger.debug('Selected on the first playlist from shown playlists')

    def test_play_song(self):
        time.sleep(5)
        select_play = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.header_play_button)
        select_play.click()
        self.logger.debug('Playing from the Selected Playlist')

    def test_pause_song(self):
        try:
            wait_time = WebDriverWait(self.driver, 5)
            select_pause = wait_time.until(EC.presence_of_element_located((AppiumBy.XPATH, self.pause_button)))
            select_pause.click()
            self.logger.debug('Pausing from the Selected Playlist')
        except Exception as e:
            self.logger.debug(e)

    # TODO: check which device is currently connected in Spotify picker
    def test_select_device(self, device_name):
        try:
            time.sleep(2)
            connect_device = self.driver.find_element(AppiumBy.XPATH, self.select_device)
            connect_device.click()
            self.logger.debug('Selecting a device from Picker')
            device = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, device_name)
            device.click()
            self.logger.info(f'{device_name} is connected')
            time.sleep(1)
        except Exception as NoSuchElementError:
            self.logger.critical(NoSuchElementError)
        # close_device_screen = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.close_pop_up)
        # close_device_screen.click()

    def test_disconnect_device(self):
        ac = TouchAction(self.driver)
        ac.tap(None, 350, 66, 1).perform()
        self.logger.debug('Open Spotify Picker for disconnecting the device')
        disconnect_device = self.driver.find_element(AppiumBy.XPATH, self.discon_device)
        disconnect_device.click()
        self.logger.info(f'Disconnected from the device and playing from this iPhone')
        time.sleep(1)
        # close_device_screen = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.close_pop_up)
        # close_device_screen.click()

    def test_open_playing_bar(self):
        open_pl_bar = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.pl_bar)
        open_pl_bar.click()
        self.logger.info('Opening Playing Now Window')

    def test_previous_song(self):
        play_previous_song = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.previous_button)
        play_previous_song.click()
        play_previous_song.click()
        self.logger.debug('Selecting Previous song to play')

    def test_next_song(self):
        play_next_song = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.next_button)
        play_next_song.click()
        self.logger.debug('Playing Next Song')

    def change_slide_song_progress(self):
        seek_song = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.slide_song)
        get_value = seek_song.get_attribute('value')
        self.logger.info(f'Current track period is {get_value}')  # type - string
        args = {"duration": 0.2, "fromX": 30, "fromY": 593, "toX": 191, "toY": 593}
        self.driver.execute_script("mobile: dragFromToForDuration", args)
        get_value = seek_song.get_attribute('value')
        self.logger.info(f'After seeking track period is {get_value}')

    def test_change_volume(self):
        time.sleep(5)
        ac = TouchAction(self.driver)
        ac.tap(None, 350, 66, 1).perform()
        self.logger.debug('Open Spotify Picker for changing the device volume')
        time.sleep(5)
        args = {"duration": 0.2, "fromX": 53, "fromY": 755, "toX": 202, "toY": 593}
        self.driver.execute_script("mobile: dragFromToForDuration", args)
        self.logger.info('Changed volume to 50')
        time.sleep(2)
        close_device_screen = self.driver.find_element(AppiumBy.XPATH, self.close_pop_up)
        close_device_screen.click()

    def tear_down(self):
        self.driver.quit()


if __name__ == '__main__':
    username = 'xyz'
    password = '1234'
    keyword = 'Songs'
    friendly_name = 'a_b_c'  # get this name from device side
    Sp_app = Spotify_iOS()
    Sp_app.test_open_app()
    Sp_app.test_login_screen(username, password)
    value = Sp_app.test_verify_user()
    if not value:
        Sp_app.test_login_screen(username, password)
    else:
        pass
    Sp_app.test_select_device(friendly_name)
    Sp_app.test_select_song(keyword)
    Sp_app.test_play_song()
    Sp_app.test_open_playing_bar()
    Sp_app.test_change_volume()
    time.sleep(4)
    Sp_app.test_next_song()
    time.sleep(10)
    Sp_app.test_previous_song()
    time.sleep(10)
    Sp_app.test_pause_song()
    Sp_app.test_next_song()
    Sp_app.change_slide_song_progress()
    # Sp_app.test_disconnect_device()





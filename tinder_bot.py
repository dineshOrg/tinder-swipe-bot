from selenium import webdriver
from time import sleep
import os
import re
import logging
import datetime
import random
import chromedriver_binary  # Adds chromedriver binary to path

from secrets import username, password
from settings import *


current_directory = os.getcwd()
currentDT = datetime.datetime.now()
date_time = currentDT.strftime("%m%d%Y_%H%M%S")

FORMAT = '%(message)s'
log_file = os.path.join(
    current_directory, f'logs/raw_data/profile_info{date_time}.log')
logging.basicConfig(level=logging.INFO,
                    filename=log_file,
                    filemode='w',
                    format=FORMAT)
logger = logging.getLogger('tinder_bot')
# logger.info('')

num_swiped = 0


class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.num_swiped = 0

    def login(self):
        self.driver.get('https://tinder.com')

        sleep(5*random.uniform(1, 1.75))

        fb_btn = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button')
        fb_btn.click()

        sleep(1*random.uniform(1, 1.75))

        # switch to login popup
        base_window = self.driver.window_handles[0]
        self.driver.switch_to_window(self.driver.window_handles[1])

        sleep(3*random.uniform(1, 1.75))

        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(username)

        pw_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pw_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
        login_btn.click()

        self.driver.switch_to_window(base_window)

        sleep(2*random.uniform(1, 1.75))

        popup_1 = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        popup_1.click()

        sleep(0.25*random.uniform(1, 1.75))

        popup_2 = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        popup_2.click()

    def like(self):
        liked = False
        for _ in range(3):
            try:
                like_btn = self.driver.find_element_by_xpath(
                    '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/button[3]')
                like_btn.click()
                liked = True
                break
            except:
                # wait before trying again
                sleep(1*random.uniform(1, 1.75))
        if liked == False:
            print('Failed to like profile.')
            logger.warn('Failed to like profile.')
            raise Exception('Failed to like profile.')

    def dislike(self):
        disliked = False
        for _ in range(3):
            try:
                dislike_btn = self.driver.find_element_by_xpath(
                    '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/button[1]')
                dislike_btn.click()
                disliked = True
                break
            except:
                # wait before trying again
                sleep(1*random.uniform(1, 1.75))
        if disliked == False:
            print('Failed to disliked profile.')
            logger.warn('Failed to disliked profile.')
            raise Exception('Failed to disliked profile.')

    def auto_swipe(self):
        while True:
            # sleep(0.5)
            try:
                try:
                    self.open_profile()
                except BaseException:
                    logger.exception('Error opening profile')
                    sleep(1*random.uniform(1, 1.75))
                # wait for profile to load
                sleep(0.1*random.uniform(1, 2))
                info = self.get_profile_info()
                if info == 'failed to get info':
                    for _ in range(3):
                        # wait before trying again
                        sleep(0.4*random.uniform(1, 2))
                        print('Trying to get info again..')
                        logger.info('Trying to get info again..')
                        new_info = self.get_profile_info()
                        if new_info != 'failed to get info':
                            info = new_info
                            break
                #sleep(0.1*random.uniform(1, 1.75))
                if swipe_thru_images == True:
                    pics = self.download_profile_pics()
                else:
                    pics = ''
                if info != 'dislike' and pics != 'dislike':
                    self.like()
                else:
                    self.dislike()
                    print('disliked')
                    logger.info('disliked')
                self.num_swiped += 1
                print(f'Total swiped so far: {self.num_swiped}')
                logger.info(f'Total swiped so far: {self.num_swiped}')
            except Exception:
                try:
                    try:
                        self.close_popup()
                    except Exception:
                        self.close_match()
                except Exception:
                    print('continuing..')
                    logger.info('continuing..')

    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        popup_3.click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()

    def open_profile(self):
        profile_open = False
        # try to open profile 3 times
        for _ in range(3):
            try:
                profile = self.driver.find_element_by_xpath(
                    '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/button')
                profile.click()
                profile_open = True
                # leave for loop if sucess
                break
            except:
                try:
                    # when profile has extra text surrounding open profile button
                    profile = self.driver.find_element_by_xpath(
                        '//*[@id= "content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[7]/button')
                    profile.click()
                    profile_open = True
                    # leave for loop if sucess
                    break
                except:
                    try:
                        try:
                            self.close_popup()
                        except Exception:
                            self.close_match()
                    except:
                        print('Failed to open profile')
                        logger.warn('Failed to open profile')
            # wait before trying to open again
            sleep(0.4*random.uniform(1, 1.75))

        if profile_open != True:
            raise Exception('Failed to open profile.')

    def get_profile_info(self):
        dislike_profile = False
        name = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div/h1')
        if name.text == '':
            dislike_profile = 'failed to get info'
            raise Exception(dislike_profile)
        # remove special characters like emojis
        name = name.text.encode().decode(
            'unicode_escape').encode('ascii', 'ignore').decode().encode('utf-8')
        print(f'name: {name}')
        logger.info(f'name: {name}')

        try:
            age = self.driver.find_element_by_xpath(
                '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[1]/span')
            age = age.text.encode().decode('unicode_escape').encode(
                'ascii', 'ignore').decode().encode('utf-8')
            print(f'age: {age}')
            logger.info(f'age: {age}')
        except:
            if dislike_no_age == True:
                dislike_profile = 'dislike'
                logger.info('no age.. disliking..')
                print('no age.. disliking..')

        try:
            bio = self.driver.find_element_by_xpath(
                '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]')
            # remove special characters like emojis
            bio = bio.text.encode().decode('unicode_escape').encode(
                'ascii', 'ignore').decode().encode('utf-8')
            # handle cases where the bio variable grabs instagram pictures
            # and there really is no bio
            if 'Instagram Photos'.encode('utf-8') in bio:
                #raise Exception('No Bio')
                bio = bio[:bio.find("Instagram Photos\n")]
                test_bio = bio.replace(' ', '')
                if test_bio.isdigit():
                    raise Exception('No Bio')
            for stop_word in stop_words:
                if stop_word.casefold() in bio.decode('utf-8').casefold():
                    dislike_profile = 'dislike'
                    logger.info('stop word in bio.. disliking..')
                    print('stop word in bio.. disliking..')
            if bio != b'':
                print(f'bio: {bio}')
                logger.info(f'bio: {bio}')
            else:
                raise Exception('No Bio')
            if len(bio.decode('utf-8')) <= (minimum_bio_length - 1):
                dislike_profile = 'dislike'
                logger.info('minimum bio length not met.. disliking..')
                print('minimum bio length not met.. disliking..')
        except BaseException:
            if dislike_no_bio == True:
                dislike_profile = 'dislike'
                logger.info('no bio.. disliking..')
                print('no bio.. disliking..')
            print('No Bio. Bicth needs to make a bio lol.')
            #logger.exception('No Bio found..')
        return dislike_profile

    def get_picture_url(self, pic_num):
        picture_xpath = f'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/span/a[2]/div/div[1]/div/div[{pic_num}]/div/div/div'
        picture = self.driver.find_element_by_xpath(picture_xpath)
        picture_style = picture.get_attribute('style')
        picture_url = picture_style[picture_style.find(
            'url("')+len('url("'):picture_style.rfind('")')]
        for _ in range(3):
            if picture_url == '':
                print('NO PICTURE')
                sleep(0.3*random.uniform(1, 2))
                picture = self.driver.find_element_by_xpath(picture_xpath)
                picture_style = picture.get_attribute('style')
                picture_url = picture_style[picture_style.find(
                    'url("')+len('url("'):picture_style.rfind('")')]
            else:
                break
        # if still no picture
        if picture_url == '':
            raise Exception('Failed to get picture.')
        return picture_url

    def download_profile_pics(self):
        dislike_profile = False
        prev_picture_url = ''
        # swipe thru pictures
        pics = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/span/a[2]/div/div[1]/div')
        num_pics = len(pics.find_elements_by_xpath("./div"))

        if num_pics <= 1:
            if dislike_one_image == True:
                dislike_profile = 'dislike'
                logger.info('not enough images.. disliking..')
                print('not enough images.. disliking..')

        #print(f'Num pics {num_pics}')
        #logger.info(f'Num pics {num_pics}')

        for x in range(num_pics):
            try:
                pic_num = x + 1
                #print(f'On pic {pic_num}/{num_pics}')
                #logger.info(f'On pic {pic_num}/{num_pics}')
                # only click on picture if it isn't the first picture.
                if pic_num != 1:
                    picture_button = self.driver.find_element_by_xpath(
                        f'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/span/a[2]/div/div[2]/button[{pic_num}]')
                    picture_button.click()
                # pause to load dom
                sleep(0.3*random.uniform(1, 1.75))
                try:
                    picture_url = self.get_picture_url(pic_num)
                except:
                    try:
                        self.close_popup()
                    except Exception:
                        self.close_match()
                if picture_url == '' or picture_url == prev_picture_url:
                    picture_url = self.get_picture_url(pic_num)

                # if we still can't get a picture
                if picture_url == '' or picture_url == prev_picture_url:
                    #raise Exception('Failed to get picture.')
                    logger.warn('Failed to get picture.')
                    print('Failed to get picture.')
                else:
                    prev_picture_url = picture_url
                    print(picture_url)
                    logger.info(f'picture: {picture_url}')
            except BaseException:
                date_time = currentDT.strftime("%m%d%Y_%H%M%S")
                logger.exception(
                    f'{date_time} Failed to get any pictures')
        return dislike_profile
        # end swipe thru pictures

    def close_chrome(self):
        self.driver.close()


# start bot
# if the script fails to execute it might be that the browser is not in the same aspect ratio as when you copied the xpath. like if you copy the xpath while in mobile view but it is running the script in desktop view.

try:
    logger.info(f'{date_time} Starting bot...')
    bot = TinderBot()
    bot.login()
    # initial pause before swiping
    # to make sure page is fully loaded
    sleep(5*random.uniform(1.5, 2))
    bot.auto_swipe()
except BaseException:
    date_time = currentDT.strftime("%m%d%Y_%H%M%S")
    logger.exception(
        f'{date_time} Tinder bot has run into the following issue')

# close chrome
# bot.close_chrome()
date_time = currentDT.strftime("%m%d%Y_%H%M%S")
logger.info(f'{date_time} Turning off bot...')

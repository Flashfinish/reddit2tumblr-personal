import os
import praw  # reddit api
import urllib  # view websites
import time  # get time
from imgur_downloader import ImgurDownloader    #get images (specifically gifv)
import pytumblr #tumblr api
from pytube import YouTube  #youtube downloading api
import glob # for deleting things in the image folder


def read_secrets(filename):
    try:
        text = open(filename, 'r')
        lines = []
        for line in text:
            line = line.replace('\n', '')
            lines.append(line)
        text.close()
        return lines
    except:
        print('!!! Cannot find ' + filename + ' or it has been deleted !!!')


r = praw.Reddit(client_id=read_secrets('secrets_reddit')[0],  # REDDIT secrests. again don't share these
                client_secret=read_secrets('secrets_reddit')[1],
                user_agent='reddit2tumblr v.6 by rin')

client = pytumblr.TumblrRestClient(read_secrets('secrets_tumblr')[0],  # TUMBLR secrets. don't share
                                   read_secrets('secrets_tumblr')[1],
                                   read_secrets('secrets_tumblr')[2],
                                   read_secrets('secrets_tumblr')[3])

# SETTINGS
blog_name = '30-minute-memes'  # your blog name on the url www.BLOGNAME.tumblr.com

subreddit = r.subreddit("funny+meirl+me_irl+AdviceAnimals+teenagers+HistoryMemes+anime_irl+bikibottomtwitter+blackpeoplegifs+blackpeopletwitter+comedycemetery+instant_regret+dankmemes+humor+meme_irl+memes+wholesomememes+surrealmemes+DeepFriedMemes+tumblr+ComedyNecrophilia+bonehurtingjuice+trippinthroughtime+bonehurtingjuice+wholesomebpt+youdontsurf+fakehistoryporn+PornhubComments+hmmm+dank_meme+2juicy4bones+deepfriedsurrealmemes+Patrig+whothefuckup+anthologymemes+equelMemes+OTMemes+PrequelMemes+whitepeoplegifs+SequelMemes+WhitePeopleTwitter+youtubehaiku+NotTimAndEric+InterdimensionalCable+gifs+combinedgifs+HighQualityGifs+reactiongifs+reallifedoodles+")     # subreddit(s) you want to grab posts from. if you want to do more than one do "sub1+sub2"

min_score = 50  # min score a post can have to post

post_limit = 300    # number of posts you want to upload. if it fails to upload it still counts

post_sort = 'day'   # how to tell reddit to sort them

delete_images_when_done = False  # if you want the program to delete everything in the images folder when its done


def unic(msg):  # convert text for saving in .txt
    return msg.encode("utf-8")


def getTags(redsub):    # input subreddit and
    print("Input Sub: " + str.lower(str(redsub)))

    normal = ["meme", "memes", "dank", "funny", "lol", "humor", "humour", "lmao", "dank meme", "dank memes", "super dank", "lolz", "funny pics", "funny post", "funny", "lmfao", "me_irl", "30minute"]

    starwars = ["star wars", "starwars", "star wars memes", "starwars memes", "prequelmemes", "prequel memes", "sequel memes"]

    history = ["history", "history memes", "fake history", "fake history porn", "funny history"]

    surreal = ["surreal", "surreal memes", "weird memes", "wierd memes", "deep fried memes", "fired memes"]

    wholesome = ["wholesome", "wholesome memes", "nice memes"]

    twitter = ["twitter memes", "black people twitter", "white people twitter", "funny twitter"]

    anime = ["anime memes", "anime", "funny anime", "animememes", "animemes"]

    stockphoto = ["stockphoto memes", "stock photo memes", "stock photo", "stock photos"]

    chan = ["4chan", "greentext", "green text"]

    hmmm = ["hm", "hmm", "hmmm", "hmmmm", "makes you think", "think", "wierd", "weird"]

    youtube = ["youtube", "video", "gif", "gifs", "funny videos", "videos", "meme video"]

    gifs = ["gif", "gifs", "funny gif", "funny gifs", "jif", "high quality gifs"]

    tags = normal
    redsub = str(redsub)

    # STAR WARS MEMES
    if str.lower(redsub) == 'anthologymemes' or str.lower(redsub) == 'equelmemes' or str.lower(redsub) == 'otMemes' or str.lower(redsub) == 'prequelmemes' or str.lower(redsub) == 'sequelmemes':
        print("Output Tags: STAR WARS")
        tags.extend(starwars)


    # HISTORY MEMES
    if str.lower(redsub) == 'mistoryMemes' or str.lower(redsub) == 'trippinthroughtime' or str.lower(redsub) == 'fakehistoryporn':
        print("Output Tags: HISTORY")
        tags.extend(history)

    # SURREAL MEMES / DEEP FRIED MEMES
    if (str.lower(redsub) == 'deepfriedmemes' or str.lower(redsub) == 'deepfriedsurrealmemes' or str.lower(redsub) == 'surrealmemes' or str.lower(redsub)) == 'whothefuckup':
        print("Output Tags: SURREAL")
        tags.extend(surreal)

    # WHOLESOME MEMES
    if str.lower(redsub) == 'wholesomememes' or str.lower(redsub) == 'wholesomebpt':
        print("Output Tags: WHOLESOME")
        tags.extend(wholesome)

    # TWITTER MEMES
    if str.lower(redsub) == 'bikibottomtwitter' or str.lower(redsub) == 'blackpeopletwitter' or str.lower(redsub) == 'whitepeopletwitter':
        print("Output Tags: TWITTER")
        tags.extend(twitter)

    # ANIME MEMES
    if str.lower(redsub) == 'anime_irl':
        print("Output Tags: ANIME")
        tags.extend(anime)

    # STOCK PHOTO MEMES
    if str.lower(redsub) == 'youdontsurf':
        print("Output Tags: YOUDONTSURF")
        tags.extend(stockphoto)

    # 4CHAN MEMES
    if str.lower(redsub) == '4chan':
        print("Output Tags: 4CHAN")
        tags.extend(chan)

    # YOUTUBE / VIDEO
    if str.lower(redsub) == 'youtubehaiku' or str.lower(redsub) == 'nottimanderic' or str.lower(redsub) == 'interdimensionalcable':
        print('Output Tags: YouTube / Video')
        tags.extend(youtube)

    # GIFS
    if str.lower(redsub) == 'gifs' or str.lower(redsub) == 'combinedgifs' or str.lower(redsub) == 'highqualitygifs' or str.lower(redsub) == 'reactiongifs' or str.lower(redsub) == 'reallifedoodles' or str.lower(redsub) == 'instant_regret' or str.lower(redsub) == 'whitepeoplegifs':
        print('Otput Tags: GIFS')
        tags.extend(gifs)

    # HMMM MEMES
    if str.lower(redsub) == "hmmm":
        print('Output Tags: HMMM')
        tags.extend(hmmm)

    if tags == normal:
        print('Output Tags: NORMIE')

    return tags


def q_post(file_name, file_type, subreddit, caption):  # i made q_post it's own function because i'm lazy and don't want to type out this post thing so much
    if file_type == 'photo':
        client.create_photo(blog_name, caption=caption, state='queue', tags=getTags(subreddit), data=file_name)
    elif file_type == 'video':
        client.create_video(blog_name, caption=caption, state='queue', tags=getTags(subreddit), data=file_name)
    else:
        print('Only photo and video supported currently')


def main():

    # Initializing
    current_dir = os.path.dirname(os.path.realpath(__file__))  # pytube download requires a full file path and using this to get it



    print("opening file..")  # open output in writing mode
    target = open("output.txt", "w")

    print("removing file..")  # reset output
    target.truncate()

    print("writing file..")

    print('getting submission')
    submissions = subreddit.top(post_sort, limit=post_limit)  # can be 'day' 'week' 'month' 'year' and probably 'all'e
    print('obtianed submission')
    with open('cache.txt', 'r') as cache:  # go through all the cached posts
        existing = cache.read().splitlines()

    with open('cache.txt', 'a+') as cache:  # with cache open
        for submission in submissions:  # go through all submissions gathered
            time.sleep(.025)  # wait so i can watch it work
            if submission.id not in existing and submission.score >= min_score:     # if we don't have it and it has enough points

                # Adding to cache
                existing.append(submission.id)      # writes down the submission id so we post it again
                cache.write(submission.id + '\n')

                # Image sites
                if submission.domain == 'i.imgur.com' or submission.domain == 'm.imgur.com' or submission.domain == 'imgur.com' or submission.domain == 'i.reddit.com' or submission.domain == 'i.redd.it':

                    # GIFs (but not GIFV)
                    if '.gif' in submission.url and '.gifv' not in submission.url:
                        print('\n______________________________\n')
                        print('File format: GIF')
                        urllib.request.urlretrieve(submission.url, 'images/' + submission.id + '.gif')
                        q_post('images/' + submission.id + '.gif', 'photo', submission.subreddit, submission.title)
                        # continue

                    # JPG
                    elif '.jpg' in submission.url:
                        print('\n______________________________\n')
                        print('File format: JPG')
                        urllib.request.urlretrieve(submission.url, 'images/' + submission.id + '.jpg')
                        q_post('images/' + submission.id + '.jpg', 'photo', submission.subreddit, submission.title)
                        # continue

                    # PNG
                    elif '.png' in submission.url:
                        print('\n______________________________\n')
                        print('File Format: PNG')
                        urllib.request.urlretrieve(submission.url, 'images/' + submission.id + '.png')
                        q_post('images/' + submission.id + '.png', 'photo', submission.subreddit, submission.title)
                        # continue

                    # JPEG
                    elif '.JPEG' in submission.url:
                        print('\n______________________________\n')
                        print('File Format: JPEG')
                        urllib.request.urlretrieve(submission.url, 'images/' + submission.id + '.JPEG')
                        q_post('images/' + submission.id + '.JPEG', 'photo', submission.subreddit, submission.title)
                        # continue

                # YouTube
                elif submission.domain == 'youtu.be' or submission.domain == 'youtube.com':

                    print('\n______________________________\n')
                    print('File Format: Video (YouTube)')
                    try:
                        os.system('youtube-dl ' + submission.url + ' -o images/' + submission.id + '.mp4')
                    except:
                        print('!!! Could not download YouTube video !!!')
                        # continue

                    # this if elif is if the video came from youtubehaiku
                    # they put stuff like this in front of the name, so i remove it
                    new_title = submission.title
                    if '[poetry]' in str.lower(submission.title):
                        new_title = submission.title[9:]
                    elif '[haiku]' in str.lower(submission.title):
                        new_title = submission.title[8:]
                    q_post(current_dir + '/images/' + submission.id + '.webm', 'video', submission.subreddit, new_title)
                    # continue

                # GFYCAT
                elif '.gifv' in submission.url and submission.domain == 'gfycat.com':
                    print('\n______________________________\n')
                    print('File Format: GIF (GFYCAT)')
                    # gotta do substrings because the link reddit gives is wrong 100% of the time
                    gfycat_d = submission.url[:8] + 'thumbs.' + submission.url[8:] + '-size_restricted.gif'
                    try:
                        urllib.request.urlretrieve(gfycat_d, 'images/' + submission.id + '.gif')
                    except:
                        print("!!! Tried to download GFYCAT, failed !!!")
                        # continue
                    q_post('images/' + submission.id + '.gif', 'photo', submission.subreddit, submission.title)
                    # continue

                # v.reddit.com
                elif submission.domain == 'v.reddit.com':
                    print('\n______________________________\n')
                    print('File format: Video (v.reddit)')
                    try:
                        os.system('youtube-dl ' + submission.url + ' -o images/' + submission.id + '.mp4')
                    except:
                        print('!!! Could not download Reddit video !!!')
                        # continue

                    q_post('images/' + submission.id + '.mp4', 'video', submission.subreddit, submission.title)
                    # continue

            else:
                print('Already have ' + submission.id + '!')



    if delete_images_when_done:
        folder = current_dir + '/images/*'
        files = glob.glob(folder)
        for f in files:
            os.remove(f)

        print('Images folder cleared')
    print('!!! DONE STEALING MEMES !!!')
    target.close()  # unload the text
    input()


if __name__ == "__main__":
    main()

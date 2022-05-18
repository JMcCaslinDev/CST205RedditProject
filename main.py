# CST 205
# Reddit Image Processor Bot
# Abstract: This program takes in an image and text from our imageProccessing subreddit we created. The program applies the image filter specified by the posts title, to the user input image. The edited image is then reposted to the subreddit via our groups bot's reddit account. This reddit account is needed for reddit api authentication and is used to pull data and post output data to our subreddit we created.
# Diego Ponce, Cooper Steiner, Jonathan McCaslin
# Github: https://github.com/jmccaslin21/CST205RedditProject
#Post an image to the subreddit with the desired filter as the title 

#Instructions: This program needs to be actively running and uses authentication with reddits api. This means that it may not workif two versions run at the same time. So we have hosted our code running on a loop so its running in hte backround. To access the programs inputs go to https://www.reddit.com/r/ImageProccessingCS205/ and follow the post instruction requriments in our subreddit with the proper title restirctions to see the functionality of our programs code.

#while this program runs post to the subreddit and wait for an automatic post response with your output

#if this code breaks and stops auto running then you can run it manually from the guthub yourself since only one of these should probably be running at one time

import praw
import os, re, requests
import json
from PIL import Image
import time
import numpy as np



def returnJsonDictObject(filename):#string attribute
  #check if file empty
  if(os.stat(filename).st_size != 0):
    #open json file
    with open(filename, 'r') as access_json:
       #read_content given info from json
      read_content = json.load(access_json)
  #returns dict object 
  return read_content


  
def returnRedditInstance():
    jData = returnJsonDictObject('Credentials.json')
    reddit = praw.Reddit(
        client_id=jData.get('client_id'),
        client_secret=jData.get('client_secret'),
        password=jData.get('password'),
        user_agent=jData.get('user_agent'),
        username=jData.get('username'),)
    return reddit


def downloadImageFromSubreddit(submission):
    url = (submission.url)
    file_name = url.split("/")
    if len(file_name) == 0:
        file_name = re.findall("/(.*?)", url)
    file_name = file_name[-1]
    if "." not in file_name:
        file_name += ".jpg"
    print(file_name)
    r = requests.get(url)
    with open(file_name,"wb") as f:
        f.write(r.content)



def main():
  Run = True
  while(Run == True):
    reddit = returnRedditInstance()
  
    #reddit.subreddit("FreeKarma4You")(new)
  
    for submission in reddit.subreddit('ImageProccessingCS205').new(limit = 10):
      if submission.id == "ur7gqk":
        continue
        
      if "Output" in submission.url:
        continue
        
      
      choice = submission.title
      try:
        url = submission.url
      except:
        print("\nImage url not found or inproper\n")
    
      image = returnImageFromUrl(url)
  
      if (choice == "grayscale"):
        image = grayscale(image)
        title = "Output Grayscale"
        #print("grayscale")
        post(image, submission, reddit, title)
        
      elif(choice == "sepia"):
        image = sepia(image)
        title = "Output Sepia"
        #print("sepia")
        post(image, submission, reddit, title)
        
      elif(choice == "negative"):
        image = negative(image)
        title = "Output Negative"
        #print("negative")
        post(image, submission, reddit, title)
  
      elif(choice == "scale down"):
        image = scaleDown(image)
        title = "Output scale down"
        #print("scale down")
        post(image, submission, reddit, title)
  
    print("sleeping 5 seconds")
    time.sleep(5)
    print("\n")  
#end of main


def returnListFromTextFile(filename):#string
  #takes in .txt name outputs file as list
  if not os.path.isfile("postsRepliedTo.txt"):
    posts_list = []
    return posts_list
    
  with open("postsRepliedTo.txt", "r") as f:
    posts_list = f.read() 
    posts_list = posts_list.split("\n")
      
    posts_list = list(filter(None, posts_list))
  #return file as list object  
  return posts_list



def writePostsRepliedToFile(postsRepliedTo):
  with open("postsRepliedTo.txt", "w") as f:
    for x, postId in enumerate(postsRepliedTo):
      if(x != -1):
        f.write(postId + "\n")
      else:
        f.write(postId)

        

def post(image, submission, reddit,title):
      posts_list = returnListFromTextFile("postsRepliedTo.txt")

      if submission.id in posts_list:
        #print("already processed image")
        return

  
      
      image.save("images/resultImage.png")



  
      
      images = "images/resultImage.png"
      subreddit = reddit.subreddit("ImageProccessingCS205")
      subreddit.validate_on_submit = True
      
      try:
        subreddit.validate_on_submit = True
        subreddit.submit_image(title, images)
        print("post posted!!")
        posts_list.append(submission.id)
  
        writePostsRepliedToFile(posts_list)
        
      except praw.exceptions.APIException as e:
        #Ratelimit hit when posting path
        print(e)
        print("\nrateLimit posting error need to add time locks \n")



        

def returnImageFromUrl(url):
  image = Image.open(requests.get(url, stream=True).raw)
  return image
  
#api to pixel function
def conv_pic_to_pix(img):
  im2 = Image.open(requests.get(img, stream=True).raw)
  pix = im2.getdata()
  print(list(pix))
  return pix



#Image filtering functions
def grayscale(img):
  width, height = img.size
  new_list = [ ( (a[0]+a[1]+a[2])//3, ) * 3
                    for a in img.getdata() ]
  return_image = Image.new('RGB', (width, height))
  return_image.putdata(new_list)
  return return_image

def sepia(img):
  width, height = img.size
  #print(width + " " + height)
  return_image = Image.new('RGB', (width, height))
  all_pixels = [(sepia_pixel(p)) for p in img.getdata()]
  return_image.putdata(all_pixels)
  return return_image

# https://stackoverflow.com/questions/36434905/processing-an-image-to-sepia-tone-in-python

def sepia_pixel(p):
  sepiaRed = 0.393 * p[0] + 0.769 * p[1] + 0.189 * p[2]
  sepiaGreen = 0.349 * p[0] + 0.686 * p[1] + 0.168 * p[2]
  sepiaBlue = 0.272 * p[0] + 0.534 * p[1] + 0.131 * p[2]
  return (int(sepiaRed), int(sepiaGreen), int(sepiaBlue))


def sepia_indv_pix(p):
  # tint shadows
  if p[0] < 63:
     r,g,b = int(p[0] * 1.1), p[1], int(p[2] * 0.9)
  
  # tint midtones
  elif p[0] > 62 and p[0] < 192:
     r,g,b = int(p[0] * 1.15), p[1], int(p[2] * 0.85)
  
  # tint highlights
  else:
     r = int(p[0] * 1.08)
     g,b = p[1], int(p[2] * 0.5)
  
  return (r,g,b)



def negative(img):
  width, height = img.size
  negative_list = [(255-p[0], 255-p[1], 255-p[2])
                            for p in img.getdata()]
  return_image = Image.new('RGB', (width, height))
  return_image.putdata(negative_list)
  return return_image

def scaleDown(img):
    w, h = img.width//2, img.height//2
    return_image = Image.new('RGB', (w, h))
    target_x = 0
    for source_x in range(0, img.width, 2):
        target_y = 0
        for source_y in range(0, img.height, 2):
            p = img.getpixel((source_x, source_y))
            return_image.putpixel((target_x, target_y), p)
            target_y += 1
        target_x += 1
        
    return return_image

def scaleUp(img):

    mf = 2
    w, h = img.width*mf, img.height*mf

    my_trgt = Image.new('RGB', (w, h))
    target_x = 0
    for source_x in np.repeat(range(img.width), mf):
       target_y = 0
       for source_y in np.repeat(range(img.height), mf):
           p = img.getpixel((int(source_x), int(source_y)))
           my_trgt.putpixel((target_x, target_y), p)
           target_y += 1
       target_x += 1

    return my_trgt

    
























#needs to be last line of file
if __name__ == '__main__':
  main()
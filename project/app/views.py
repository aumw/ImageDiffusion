from django.shortcuts import render, redirect
from .models import Profile, Prompt
from django.contrib import messages
from .forms import PromptForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from pathlib import Path
import os


import argparse
import sys
import os
import numpy as np
sys.path.append('./')
import torch
from diffusers import StableDiffusionPipeline,  StableDiffusionImg2ImgPipeline 

import PIL
import requests
from io import BytesIO

from diffusers import StableDiffusionInpaintPipeline
from PIL import Image


# Create your views here.
def home(request):
	if (request.user.is_authenticated):
		form = PromptForm(request.POST or None, request.FILES or None)
		if request.method == 'POST':
			if form.is_valid():
				prompt = form.save(commit=False)
				prompt.user = request.user
				form.save()
				path = "../project" + prompt.original_image.url
				messages.success(request, ("Check the gallery!!"))
				outdir = "media/outputs/img2img-samples/{}".format(prompt.prompt.replace(" ", "_"))
				output_dir, output_images = sample(ckpt="nitrosocke/Ghibli-Diffusion", from_file=None, prompt=prompt.prompt, image_path=path, batch_size=1, num_images=1, outdir=outdir, random_seed=0, step=70, device="cuda:0")
				# OutputImage.objects.create(prompt=prompt, output_image=output_dir)
				prompt.diffused_image = output_dir
				prompt.save(update_fields=["diffused_image"])

				return redirect('home')


		# prompts = Prompt.objects.all().order_by("-created_at")
		prompts = Prompt.objects.filter(user_id=request.user).last()
		# output_image = OutputImage.objects.get(prompt=prompts)
		return render(request, 'home.html', {"prompts":prompts, "form":form})

	else:
		prompts = Prompt.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"prompts":prompts})

def profile_list(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)
		return render(request, 'profile_list.html', {"profiles":profiles})
	else:
		messages.success(request, ("You Must Be Logged In To Use This Page"))
		return redirect('home')




def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)

		prompts = Prompt.objects.filter(user_id=pk).order_by("-created_at")

		# output_objects = OutputImage.objects.all()


		return render(request, "profile.html", {"profile":profile, "prompts":prompts})
	else:
		messages.success(request, ("You Must Be Logged In To Use This Page"))
		return redirect('home')




def login_user(request):


	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			messages.success(request, ("You have been logged in!"))
			return redirect('home')
		else:
			messages.success(request, ("Incorrect Username or Password"))
			return redirect('login')

	else:
		return render(request, 'login.html', {})




def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out"))
	return redirect('home')


def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']

			user = authenticate(username=username, password=password)
			login(request, user)

			messages.success(request, ("You have been successfully registered"))
			return redirect('home')
		# else:
		# 	messages.success(request, ("Something went wrong"))
		# 	return redirect('register')

	
		
	return render(request, 'register.html', {"form":form})





def sample(ckpt, from_file, prompt, image_path, batch_size, num_images=5, outdir="", random_seed=0, step=50, device="cpu"):

    torch.manual_seed(random_seed)
    np.random.seed(random_seed)
    model_id = ckpt
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, safety_checker=None).to(device)
    os.makedirs(outdir, exist_ok=True)
    if prompt is not None:
        prompts = prompt.split(',')
    else:
        print(f"reading prompts from {from_file}")
        with open(from_file, "r") as f:
            prompts = f.read().splitlines()
    if type(image_path) == str:
        init_image = Image.open(image_path).convert("RGB")
        init_image.thumbnail((768, 768))
    else:
        init_image = image_path
    output_dir = []
    output_img = []
    for prompt in prompts:
        print(f"generating images for prompt: {prompt}")
        dirname = '_'.join(prompt[:50].split()) 
        outpath = outdir + dirname
        os.makedirs(outpath, exist_ok=True)
        output_dir = outpath
        all_images = []
        num_batch = int(num_images) // batch_size
        for batch in range(num_batch):
            images = pipe([prompt] * batch_size, [init_image] * batch_size, num_inference_steps=step, strength=0.75, guidance_scale=7.5, eta=1.).images
            all_images += images
            images_sep = [Image.fromarray(np.array(x)) for x in images]
            output_img.extend(images_sep)
            names = ['_'.join(prompt[:50].split()) + '_' + str(batch * batch_size + i) for i in range(batch_size)]
            for im, name in zip(images_sep, names):
                im.save(outpath + '/{}.png'.format(name))
            images = np.hstack([np.array(x) for x in images])
            images = Image.fromarray(images)
            # takes only first 50 characters of prompt to name the image file
            name = '-'.join(prompt[:50].split()) + "-samples"
            if random_seed == 0:
                images.save(outpath + '/{}.png'.format(name))
            output_dir = outpath + '/{}.png'.format(name)
    return output_dir, output_img


def parse_args():
    parser = argparse.ArgumentParser('', add_help=False)
    parser.add_argument('--ckpt', help='target string for query',
                        type=str)
    parser.add_argument('--from-file', help='path to prompt file', default='./data',
                        type=str)
    parser.add_argument('--prompt', help='prompt to generate', default=None,
                        type=str)
    parser.add_argument("--image_path", default="./data", type=str)
    parser.add_argument("--batch_size", default=5, type=int)
    parser.add_argument('--num_images', default=5, help="number of image for one prompt", type=int)
    parser.add_argument("--outdir", type=str, default="")
    parser.add_argument("--random_seed", default=0, type=int)
    parser.add_argument("--step", default=50, type=int)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    sample(args.ckpt, args.from_file, args.prompt, args.image_path, args.batch_size, args.num_images, args.outdir, random_seed=args.random_seed, step=args.step)





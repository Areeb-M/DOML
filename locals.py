DOCSTRING = '''

Welcome to D.O.M.L

Discord
Owns
My
Life

Purpose: a Discord bot that integrates the various social communication outlets in my life into a Discord Server

Features: GroupMe, MUDs, 

'''

# Imports
import discord
import requests
import io


# Data Loading Functions
TOKEN_DISCORD = open("data/token_discord.txt").readline()
TOKEN_GROUPME = open("data/token_groupme.txt").readline()
USERID_GROUPME = open("data/userid_groupme.txt").readline()
NAME_DISCORD = open("data/name_discord.txt").readline()


def retrieve_group_data():
    # Returns a list of all the lines in the group data file
    data = []
    try:
        file = open("data/list_groups.txt")
        data = file.readlines()
        file.close()
    except FileNotFoundError:
        print("Group List data file not found. Generating an empty file!")
        open("data/list_groups.txt", "w+").close()

    return data

# Data Storage Functions


def store_group_data(server_list):
    file = open("data/list_groups.txt", 'w')
    for server in server_list:
        file.write(str(server)+"\n")
    file.close()


def append_group_data(server):
    file = open("data/list_groups.txt", 'a')
    file.write(str(server)+"\n")
    file.close()

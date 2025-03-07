import sys, os, json, time, urllib3

from Config import Variable

http = urllib3.PoolManager()


def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    
def gradient_text(text, start_color = Variable.pink, end_color=Variable.purple):
    start_r, start_g, start_b = start_color
    end_r, end_g, end_b = end_color
    length = len(text)

    gradient_text = ""
    for i, char in enumerate(text):
        r = start_r + (end_r - start_r) * i // length
        g = start_g + (end_g - start_g) * i // length
        b = start_b + (end_b - start_b) * i // length
        gradient_text += f"\033[38;2;{r};{g};{b}m{char}"
    
    return gradient_text + "\033[0m" 

with open("./config/config.json", "r") as f:
    x = json.load(f)
    if x["First_Launch"] == True:
        print(gradient_text("First Launch detected\nPlease fill in the following information"))
        username = input(gradient_text("How would you like us to call you? (This will be showned as ")+  "\033[32mname:~$ \033[0m")
        
        x["First_Launch"] = False
        x["username"] = username
        with open("./config/config.json", "w") as f:
            json.dump(x, f, indent=4)
            
import urllib3
import json

def check_valid_webhook(webhook):
    try:
        http = urllib3.PoolManager()
        
        response = http.request("GET", webhook)
        
        if response.status // 100 != 2:
            return False, f"Webhook returned status code: {response.status}"
        
        try:
            data = json.loads(response.data.decode('utf-8'))
            return True, data
        except json.JSONDecodeError:
            return True, response.data.decode('utf-8')
    
    except urllib3.exceptions.HTTPError as e:
        return False, f"HTTP error occurred: {e}"
    except Exception as e:
        return False, f"Error checking webhook: {e}"
    
def update_config():
    try:
        with open("./config/config.json", "r") as f:
            x = json.load(f)
        username = input(gradient_text("How would you like us to call you? (This will be showned as ")+  "\033[32mname:~$ \033[0m")
        x["First_Launch"] = False
        x["username"] = username
        with open("./config/config.json", "w") as f:
            json.dump(x, f, indent=4)
        
        return True,""
    except Exception as e:
        return False, e

def modify_webhook(webhook_id, name=None, avatar=None, channel_id=None, webhook_token=None):
    url = f"https://discord.com/api/v10/webhooks/{webhook_id}/{webhook_token}"
    
    headers = {
        "Content-Type": "application/json",
    }
    
    data = {}
    if name:
        data["name"] = name
    if avatar:
        data["avatar"] = avatar
    if channel_id:
        data["channel_id"] = channel_id

    if data:
        body = json.dumps(data).encode('utf-8')
        
        response = http.request('PATCH', url, body=body, headers=headers)
        
        return json.loads(response.data.decode('utf-8'))
    else:
        return {"error": "No data provided for modification"}

def send_webhook_message(webhook_id, webhook_token, message, username=None, avatar=None, embeds=None, attachments=None, spam=False, wait_time=0.2):
    url = f"https://discord.com/api/v10/webhooks/{webhook_id}/{webhook_token}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "content": message
    }

    if embeds:
        data["embeds"] = embeds
    
    body = json.dumps(data).encode('utf-8')

    def send_message():
        response = http.request('POST', url, body=body, headers=headers)
        if response.status != 204:
            print(gradient_text("Failed to send message. Status code:", response.status))
        else:
            print(gradient_text("Message sent successfully."))
        return response

    if spam:
        print(f"Sending {message} times with {wait_time*1000} ms wait time...")
        while True:
            send_message()
            time.sleep(wait_time) 
    else:
        response = send_message()
        return json.loads(response.data.decode('utf-8'))

def delete_webhook(webhook_id, webhook_token):

    url = f"https://discord.com/api/v10/webhooks/{webhook_id}/{webhook_token}"
    
    headers = {
        "Content-Type": "application/json",
    }

    response = http.request('DELETE', url, headers=headers)

    if response.status == 204:
        return {"message": "Webhook deleted successfully."}
    else:
        return {"error": f"Failed to delete webhook. Status code: {response.status}"}

def create_embed():
    embed = {}
    
    embed["title"] = input(gradient_text("Enter the embed title (optional): "))
    embed["type"] = "rich"
    embed["description"] = input(gradient_text("Enter the embed description (optional): "))
    embed["url"] = input(gradient_text("Enter the embed URL (optional): "))
    embed["timestamp"] = input(gradient_text("Enter the timestamp for the embed (ISO8601 format, optional): "))
    embed["color"] = int(input(gradient_text("Enter the color code for the embed (integer, optional): "), 16) if input(gradient_text("Enter the color code for the embed (optional, HEX): ")) else 0)
    
    footer_text = input(gradient_text("Enter the footer text (optional): "))
    footer_icon = input(gradient_text("Enter the footer icon URL (optional): "))
    if footer_text:
        embed["footer"] = {"text": footer_text, "icon_url": footer_icon}
    
    image_url = input(gradient_text("Enter the image URL for the embed (optional): "))
    if image_url:
        embed["image"] = {"url": image_url}
    
    thumbnail_url = input(gradient_text("Enter the thumbnail URL for the embed (optional): "))
    if thumbnail_url:
        embed["thumbnail"] = {"url": thumbnail_url}
    
    video_url = input(gradient_text("Enter the video URL for the embed (optional): "))
    if video_url:
        embed["video"] = {"url": video_url}
    
    provider_name = input(gradient_text("Enter the provider name (optional): "))
    provider_url = input(gradient_text("Enter the provider URL (optional): "))
    if provider_name:
        embed["provider"] = {"name": provider_name, "url": provider_url}
    
    author_name = input(gradient_text("Enter the author name (optional): "))
    author_url = input(gradient_text("Enter the author URL (optional): "))
    author_icon_url = input(gradient_text("Enter the author icon URL (optional): "))
    if author_name:
        embed["author"] = {"name": author_name, "url": author_url, "icon_url": author_icon_url}
    
    fields = []
    add_fields = input(gradient_text("Do you want to add fields to the embed? (y/n): ")).lower() == 'y'
    while add_fields:
        field_name = input(gradient_text("Enter the field name: "))
        field_value = input(gradient_text("Enter the field value: "))
        inline = input(gradient_text("Is this field inline? (y/n): ")).lower() == 'y'
        fields.append({"name": field_name, "value": field_value, "inline": inline})
        
        add_fields = input(gradient_text("Do you want to add another field? (y/n): ")).lower() == 'y'
    
    if fields:
        embed["fields"] = fields
    
    return embed

if __name__ == "__main__":
    while True:
        while True:
            cls()

            print(gradient_text(Variable.banner))
            while True:
                
                try:
                    choosen_Option = int(input(gradient_text("What would you like to do?\nChoose from the following options: \n- [1] Change config\n- [2] Use the discord webhook tools\n[3] Open github repository\n- [4] Exit\n") + f"\033[32m{x['username']}:~$ \033[0m" +"-> "))
                    break
                except:
                    input(gradient_text("Invalid Option. Please try again, press enter to continue."))
                    cls()
                    print(gradient_text(Variable.banner))
                    
            
            if choosen_Option == 1:
                if update_config()[0] == True:
                    input(gradient_text("Config updated successfully. Press enter to continue."))
                    time.sleep(1)
                    break
                else:
                    input(gradient_text("Failed to update config please retry\nfeel free to open an issue on github with this error:\n"+str(update_config()[1]) + "\n\nPress enter to continue"))
                    break
                
            elif choosen_Option == 2:
                webhook = input(f"\033[32m{x['username']}:~$ \033[0m" + gradient_text("Input webhooks url -> "))
                output = check_valid_webhook(webhook)
                if output[0] == True:
                    
                    print(gradient_text("Webhook is valid. Continuing..."))
                    cls()
                    while True:
                        print(gradient_text(Variable.banner))
                        print("\033[32m{x['username']}:~$ \033[0m" + gradient_text(f"Logged in as: {output[1]['name']}\nWebhook Information:"))
                        
                        print(gradient_text("=" * 120))
                        
                        for key, value in output[1].items():
                            if value is None:
                                value = "None"
                            else:
                                value = str(value)
                                
                            
                            
                            if key == "avatar" and value == "None":
                                value = "No Avatar Set"
                            elif key == "avatar" and value != "None":
                                value = f"https://cdn.discordapp.com/avatars/{output[1]['id']}/{output[1]['avatar']}.webp"
                            if len(value) > 100:
                                value = value[:100] + "..."
                            
                            if key in Variable.known_keys:
                                print((f"\033[0m|" +f"\033[34m{key:<20} \033[0m"+f": \033[35m{value:<100} |"))
                            else:
                                print((f"| \033[33mUnknown Key: \033[31m\"{key}\": \033[0m\"{value}\" |"))
                        
                        print(gradient_text("=" * 120))
                        
                        

                        next_action = input(f"\033[32m{x['username']}:~$ \033[0m" + gradient_text("What would you like to do next?\n[1] Modify webhook\n[2] Delete webhook\n[3] Send a message\n[4] Go back\n[5] Exit\n-> "))
            
                        if next_action == '1':
                            new_name = input(f"\033[32m{x['username']}:~$ \033[0m" + gradient_text("Enter new webhook name (leave blank to keep the same): "))
                            new_avatar = input(f"\033[32m{x['username']}:~$ \033[0m" + gradient_text("Enter new avatar URL (leave blank to keep the same): "))
                            new_channel = None
                            
                            response = modify_webhook(
                                webhook_id=output[1]['id'],
                                name=new_name if new_name else None,
                                avatar=new_avatar if new_avatar else None,
                                channel_id=new_channel if new_channel else None,
                                webhook_token=output[1]['token']
                            )
                            
                            print(gradient_text("Webhook modified successfully. New details:"))
                            print(gradient_text(json.dumps(response, indent=2)))
                            input(gradient_text("Press enter to continue."))
                        elif next_action == '2':
                            confirmation = input("\033[32m{x['username']}:~$ \033[0m" +gradient_text("Are you sure you want to delete this webhook? (y/n): "))
                            if confirmation.lower() == 'y':
                                response = delete_webhook(
                                    webhook_id=output[1]['id'],
                                    webhook_token=output[1]['token']
                                )
                                print(gradient_text((response.get("message", response.get("error")))))
                                input(gradient_text("Press enter to continue."))
                                break
                            else:
                                print(gradient_text("Webhook not deleted."))
                                input(gradient_text("Press enter to continue."))
                        elif next_action == '3':
                            message = input(gradient_text("Enter the message to send: "))
                            
                            include_embeds = input(f"\033[32m{x['username']}:~$ \033[0m" + gradient_text("Do you want to include embeds? (y/n): ")).lower() == 'y'
                            spam = input(f"\033[32m{x['username']}:~$ \033[0m" + gradient_text("Do you want to send infinite messages (spam)? (y/n): ")).lower() == 'y'
                            include_username = input(f"\033[32m{x['username']}:~$ \033[0m" + gradient_text("Do you want to change the webhook's username? (y/n): ")).lower() == 'y'
                            include_avatar = input(f"\033[32m{x['username']}:~$ \033[0m" + gradient_text(f"Do you want to set a custom avatar URL? (y/n): ")).lower() == 'y'
                            include_attachments = input(f"\033[32m{x['username']}:~$ \033[0m" + gradient_text("Do you want to include attachments? (y/n): ")).lower() == 'y'
                            
                            username = None
                            if include_username:
                                username = input(f"\033[32m{x['username']}:~$ \033[0m" + gradient_text(f"Enter new username for the webhook: "))
                            
                            avatar = None
                            if include_avatar:
                                avatar = input(f"\033[32m{x['username']}:~$ \033[0m" + gradient_text("Enter the new avatar URL for the webhook: "))
                            
                            embeds = None
                            if include_embeds:
                                embeds = [create_embed()] 
                            
                            wait_time = 0.2
                            if spam:
                                wait_time_input = input(f"\033[32m{x['username']}:~$ \033[0m" + gradient_text("Enter the wait time between spam messages in milliseconds (default 200ms): "))
                                if wait_time_input.isdigit():
                                    wait_time = int(wait_time_input) / 1000

                            response = send_webhook_message(
                                webhook_id=output[1]['id'],
                                webhook_token=output[1]['token'],
                                message=message,
                                username=username,
                                avatar=avatar,
                                embeds=embeds,
                                spam=spam,
                                wait_time=wait_time
                            )

                            print(f"\033[32m{x['username']}:~$ \033[0m" + gradient_text("Message sent successfully."))
                        
                        elif next_action == '3':
                            url = "https://github.com/Ramona-Flower/Discord-Webhook-Tools"
                            
                            try:
                                if sys.platform == "win32":
                                    os.system(f"start {url}")
                                elif sys.platform == "darwin":
                                    os.system(f"open -a 'Google Chrome' {url}")
                                else:
                                    os.system(f"xdg-open {url}")
                                
                                print(gradient_text(f"Opening URL: {url}"))
                            except Exception as e:
                                print(gradient_text(f"Error opening URL: {e}"))
                        elif next_action == '4':
                            break
                        
                        elif next_action == '5':
                            sys.exit()
                        else:
                            input(gradient_text("Invalid Option. Please try again, press enter to continue."))
                else:
                    print(output)
                    input(gradient_text("Webhook is invalid. Press enter to continue."))
                    break
                
            elif choosen_Option == 4:
                sys.exit()
            
            else:
                input(gradient_text("Invalid Option. Please try again, press enter to continue."))
                

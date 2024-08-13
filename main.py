import requests
import tkinter as tk
from tkinter import ttk, messagebox


# Your API key from viewdns.info (you need to register and get one)
VIEWDNS_API_KEY = "ENTER_YOUR_API_KEY"



# Function to perform reverse IP lookup using hackertarget.com API
def reverse_ip_lookup_hackertarget(ip):
   url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
   try:
       response = requests.get(url)
       response.raise_for_status()
       if "API count exceeded" in response.text:
           print("Hackertarget API quota exceeded.")
           return None
       domains = response.text.strip().splitlines()
       if domains:
           return domains
       else:
           return None
   except requests.RequestException as e:
       print(f"Error fetching data from hackertarget.com: {e}")
       return None



# Function to perform reverse IP lookup using viewdns.info API
def reverse_ip_lookup_viewdns(ip):
   url = f"https://api.viewdns.info/reverseip/?host={ip}&apikey={VIEWDNS_API_KEY}&output=json"
   try:
       response = requests.get(url)
       response.raise_for_status()
       data = response.json()
       if "response" in data and "domains" in data["response"]:
           return data["response"]["domains"]
       else:
           return None
   except requests.RequestException as e:
       print(f"Error fetching data from viewdns.info: {e}")
       return None


# Function to handle the lookup process and display results
def lookup_domains():
   ip = ip_entry.get().strip()
   if not ip:
       messagebox.showerror("Input Error", "Please enter an IP address.")
       return


   output_text.config(state='normal')
   output_text.delete(1.0, tk.END)
   output_text.insert(tk.END, f"Performing lookup for IP: {ip}\n")
   output_text.config(state='disabled')


   # Determine which API to use based on the selected option
   if api_choice.get() == "hackertarget":
       results = reverse_ip_lookup_hackertarget(ip)
       if not results:
           output_text.config(state='normal')
           output_text.insert(tk.END, "Hackertarget API returned no results or exceeded quota.\n")
           output_text.config(state='disabled')
   elif api_choice.get() == "viewdns":
       results = reverse_ip_lookup_viewdns(ip)
       if not results:
           output_text.config(state='normal')
           output_text.insert(tk.END, "ViewDNS API returned no results or an error occurred.\n")
           output_text.config(state='disabled')


   # Display results
   output_text.config(state='normal')
   if results:
       output_text.insert(tk.END, f"Domains hosted on the same server as IP {ip}:\n")
       for domain in results:
           output_text.insert(tk.END, f"{domain}\n")
   else:
       output_text.insert(tk.END, f"No valid domains found for IP {ip} or an error occurred.\n")
   output_text.config(state='disabled')




# Setup Tkinter GUI
app = tk.Tk()
app.title("Reverse IP Lookup Tool - The Pycodes")
app.geometry("600x450")


# Input Frame
input_frame = ttk.Frame(app)
input_frame.pack(pady=10)


ip_entry = ttk.Entry(input_frame, width=50)
ip_entry.pack(side=tk.LEFT, padx=5)
ip_entry.insert(0, "Enter IP address")


lookup_button = ttk.Button(input_frame, text="Lookup", command=lookup_domains)
lookup_button.pack(side=tk.LEFT, padx=5)


# API Choice Frame
api_frame = ttk.LabelFrame(app, text="Choose API")
api_frame.pack(pady=10, fill=tk.X)


api_choice = tk.StringVar(value="hackertarget")


hackertarget_radio = ttk.Radiobutton(api_frame, text="Hackertarget.com API", variable=api_choice, value="hackertarget")
hackertarget_radio.pack(side=tk.LEFT, padx=5, pady=5)


viewdns_radio = ttk.Radiobutton(api_frame, text="ViewDNS.info API", variable=api_choice, value="viewdns")
viewdns_radio.pack(side=tk.LEFT, padx=5, pady=5)


# Output Frame with Scrollbar
output_frame = ttk.Frame(app)
output_frame.pack(pady=10, fill=tk.BOTH, expand=True)


scrollbar = ttk.Scrollbar(output_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


output_text = tk.Text(output_frame, wrap=tk.WORD, state='disabled', yscrollcommand=scrollbar.set)
output_text.pack(pady=10, fill=tk.BOTH, expand=True)


scrollbar.config(command=output_text.yview)


if __name__ == "__main__":
   app.mainloop()

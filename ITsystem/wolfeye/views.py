from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import FinancialInfoForm
from .forms import IPAddressForm
from .models import CustomUser, FinancialInfo
import requests
import subprocess
from .models import ScanResult

def index(request):
    return render(request, 'wolfeye/home.html')
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #return redirect('scan_ip/')
                return render(request, 'wolfeye/scan_ip.html')
    else:
        form = AuthenticationForm()
    return render(request, 'wolfeye/login.html', {'form': form})

@login_required
def account_view(request):
    user = request.user
    financial_info = FinancialInfo.objects.get(user=user)
    return render(request, 'wolfeye/account.html', {'user': user, 'financial_info': financial_info})

def register_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        financial_form = FinancialInfoForm(request.POST)
        if user_form.is_valid() and financial_form.is_valid():
            user = user_form.save()
            financial_info = financial_form.save(commit=False)
            financial_info.user = user
            financial_info.save()

            # Payment integration with Visa
            amount = 100.0  # Example amount in USD
            currency = 'USD'
            card_number = financial_form.cleaned_data['credit_card_number']
            expiration_month = financial_form.cleaned_data['expiration_month']
            expiration_year = financial_form.cleaned_data['expiration_year']
            cvv = financial_form.cleaned_data['cvv']

            # Construct the API request payload
            payload = {
                'amount': amount,
                'currency': currency,
                'card_number': card_number,
                'expiration_month': expiration_month,
                'expiration_year': expiration_year,
                'cvv': cvv,
            }

            # Make a POST request to the Visa Direct API
            response = requests.post('https://api.visa.com/payments/v1/authorize', json=payload, headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with your API key
            })

            # Process the API response
            if response.status_code == 200:
                # Payment was successful
                transaction_id = response.json().get('transaction_id')
                # Save the transaction ID and complete the user registration
                # ...
                return render(request, 'wolfeye/registration_complete.html', {'transaction_id': transaction_id})
            else:
                # Payment failed
                error_message = response.json().get('error_message')
                #return render(request, 'payment_error.html', {'error_message': error_message})
                return render(request, 'wolfeye/registration_complete.html', {'transaction_id': '93DJ2231ADD35672D' })
                

    else:
        user_form = UserCreationForm()
        financial_form = FinancialInfoForm()

    return render(request, 'wolfeye/register.html', {'user_form': user_form, 'financial_form': financial_form})

@login_required(login_url='login')


def scan_ip(request):
    if request.method == 'POST':
        form = IPAddressForm(request.POST)
        if form.is_valid():
            ip_address = form.cleaned_data['ip_address']
            smb_scan = form.cleaned_data['smb_scan']
            smtp_scan = form.cleaned_data['smtp_scan']
            ssh_scan = form.cleaned_data['ssh_scan']
            http_scan = form.cleaned_data['http_scan']
            wordpress_scan = form.cleaned_data['wordpress_scan']
            zimbra_scan = form.cleaned_data['zimbra_scan']
            vmware_scan = form.cleaned_data['vmware_scan']


            scan_output = ''

            if smb_scan:
                import subprocess
                import shlex


                #script_path = 'smb\smb.ps1'

                # Build the PowerShell command
                #command = f'powershell -EP Bypass -File  {shlex.quote(script_path)} {shlex.quote(ip_address)}'

                # Execute the PowerShell command and capture the output
                #process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                #process.wait()
                #stdout, stderr = process.communicate()

                # Decode the output from bytes to string
                #output = stdout.decode("utf-8").strip()
                #process.wait()
                #output = subprocess.Popen(['powershell.exe', '-EP', 'Bypass', 'smb/smb.ps1', ip_address],stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                #output.wait()
                #stdout, stderr = output.communicate()
                #output = output.stdout.read().decode().strip()

                #scan_output += 'SMB Scan:\n' + f'{output}' + '\n\n'
                
                script_path = 'C:\\Users\\Sana\\Desktop\\ITSystem\\ITsystem\\wolfeye\\smb\\smb.ps1'
                # Execute the PowerShell script and capture the output
                output = subprocess.Popen(['powershell.exe', '-EP', 'Bypass', f'{script_path}', f'{ip_address}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output.wait()
                stdout = output.communicate()#scan_output += 'SMB Scan:\n' + stdout.decode('utf-8') + '\n\n'
                stdout_str = stdout[0].decode('utf-8') if stdout else ''
                scan_output += 'SMB Scan:\n' + stdout_str + '\n\n'

               

            if smtp_scan:
                script_path = 'C:\\Users\\Sana\\Desktop\\ITSystem\\ITsystem\\wolfeye\\smtp\\smb.ps1'
                # Execute the PowerShell script and capture the output
                output = subprocess.Popen(['powershell.exe', '-EP', 'Bypass', f'{script_path}', f'{ip_address}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output.wait()
                stdout = output.communicate()#scan_output += 'SMB Scan:\n' + stdout.decode('utf-8') + '\n\n'
                stdout_str = stdout[0].decode('utf-8') if stdout else ''
                scan_output += 'SMTP Scan:\n' + stdout_str + '\n\n'

            if ssh_scan:
                script_path = 'C:\\Users\\Sana\\Desktop\\ITSystem\\ITsystem\\wolfeye\\ssh\\smb.ps1'
                # Execute the PowerShell script and capture the output
                output = subprocess.Popen(['powershell.exe', '-EP', 'Bypass', f'{script_path}', f'{ip_address}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output.wait()
                stdout = output.communicate()#scan_output += 'SMB Scan:\n' + stdout.decode('utf-8') + '\n\n'
                stdout_str = stdout[0].decode('utf-8') if stdout else ''
                scan_output += 'SSH Scan:\n' + stdout_str + '\n\n'

            if http_scan:
                script_path = 'C:\\Users\\Sana\\Desktop\\ITSystem\\ITsystem\\wolfeye\\http\\smb.ps1'
                # Execute the PowerShell script and capture the output
                output = subprocess.Popen(['powershell.exe', '-EP', 'Bypass', f'{script_path}', f'{ip_address}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output.wait()
                stdout = output.communicate()#scan_output += 'SMB Scan:\n' + stdout.decode('utf-8') + '\n\n'
                stdout_str = stdout[0].decode('utf-8') if stdout else ''
                scan_output += 'HTTP Scan:\n' + stdout_str + '\n\n'

            if wordpress_scan:
                script_path = 'C:\\Users\\Sana\\Desktop\\ITSystem\\ITsystem\\wolfeye\\wordpress\\smb.ps1'
                # Execute the PowerShell script and capture the output
                output = subprocess.Popen(['powershell.exe', '-EP', 'Bypass', f'{script_path}', f'{ip_address}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output.wait()
                stdout = output.communicate()#scan_output += 'SMB Scan:\n' + stdout.decode('utf-8') + '\n\n'
                stdout_str = stdout[0].decode('utf-8') if stdout else ''
                scan_output += 'WORDPRESS Scan:\n' + stdout_str + '\n\n'

            if zimbra_scan:
                script_path = 'C:\\Users\\Sana\\Desktop\\ITSystem\\ITsystem\\wolfeye\\zimbra\\smb.ps1'
                # Execute the PowerShell script and capture the output
                output = subprocess.Popen(['powershell.exe', '-EP', 'Bypass', f'{script_path}', f'{ip_address}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output.wait()
                stdout = output.communicate()#scan_output += 'SMB Scan:\n' + stdout.decode('utf-8') + '\n\n'
                stdout_str = stdout[0].decode('utf-8') if stdout else ''
                scan_output += 'ZIMBRA Scan:\n' + stdout_str + '\n\n'

            if  vmware_scan:
                script_path = 'C:\\Users\\Sana\\Desktop\\ITSystem\\ITsystem\\wolfeye\\vmware\\smb.ps1'
                # Execute the PowerShell script and capture the output
                output = subprocess.Popen(['powershell.exe', '-EP', 'Bypass', f'{script_path}', f'{ip_address}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output.wait()
                stdout = output.communicate()#scan_output += 'SMB Scan:\n' + stdout.decode('utf-8') + '\n\n'
                stdout_str = stdout[0].decode('utf-8') if stdout else ''
                scan_output += 'VMWARE Scan:\n' + stdout_str + '\n\n'        

                

            # Save the scan result in the database
            scan_result = ScanResult(result=scan_output)
            scan_result.save()

            return render(request, 'wolfeye/scan_result.html', {'scan_output': scan_output})
    else:
        form = IPAddressForm()

    return render(request, 'wolfeye/scan_ip.html', {'form': form})

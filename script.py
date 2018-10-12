import zlib, os, glob, redis, time
from flask import Flask,jsonify,json


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route("/deflate")
def read_deflate():
    lst = []
    for compressedfilepath in os.listdir("input/"):
        with open("input/" + compressedfilepath, "rb") as f:
            decompressed = zlib.decompress(f.read())
            
            print(decompressed[0:1000])
            decompDict = {
                'result': decompressed
            }
            lst.append(decompDict)
            #jsonStr = json.dumps(lst)
    return "Done" #jsonify(Results=jsonStr)


@app.route('/')
def hello():
    count = get_hit_count()
    with open("output.txt", "a") as f:
        f.write(str(count)  + '\n')
    return 'Hello World! I have been seen {} times.\n'.format(count)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
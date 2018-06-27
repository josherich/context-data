import subprocess

def convert_chinese(text):
  return subprocess.getoutput("echo '%s' | opencc -c hk2s.json" % text)
import pygame
import os
import ncmdump

def convert_ncm_to_mp3(ncm_path, output_path):
    """将 NCM 文件转换为 MP3 格式"""
    try:
        # 使用 ncmdump 转换文件
        ncmdump.dump(ncm_path, output_path)
        return True
    except Exception as e:
        print(f"转换文件时出现错误: {e}")
        return False

# NCM 文件路径和转换后的 MP3 文件路径
ncm_file = "./music/拼图爱.ncm"  # 替换为你的 NCM 文件路径
mp3_file = ncm_file.replace('.ncm', '.mp3')

# 如果 MP3 文件不存在，则进行转换
if not os.path.exists(mp3_file):
    if not convert_ncm_to_mp3(ncm_file, mp3_file):
        print("文件转换失败")
        exit(1)

def play_music():
    # 初始化 pygame 的混音器
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(mp3_file)
        # 播放音乐，-1 表示循环播放，0 表示播放一次
        pygame.mixer.music.play(loops=-1)
        # 等待音乐播放完成
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error as e:
        print(f"播放音乐时出现错误: {e}")
    finally:
        # 退出 pygame 的混音器
        pygame.mixer.quit()
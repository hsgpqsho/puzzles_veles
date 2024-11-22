import tqdm
import os
from bit import *
from bit.format import bytes_to_wif
import multiprocessing
from multiprocessing import Pool
import atexit
import colorama
import keyboard
import random
from colorama import Fore, Back

count_dict = {'count': 0}
generating = True

filename = 'puzzles.txt'

with open(filename) as f:
    add = set(line.strip() for line in f)
print(Fore.YELLOW + f"Загружено {len(add)} пазлов.")

def seek(start, end, stop_event):
    while not stop_event.is_set():
        ran = random.randint(start, end)
        key1 = Key.from_int(ran)
        wif = bytes_to_wif(key1.to_bytes(), compressed=False)
        wif2 = bytes_to_wif(key1.to_bytes(), compressed=True)
        key2 = Key(wif)
        caddr = key1.address
        uaddr = key2.address
        myhex = "%064x" % ran
        private_key = myhex[:64]
        if caddr in add:
            print(Fore.YELLOW + f'!!!!! Пазл НАЙДЕН | {caddr} | Wif: {wif2} | Key: {private_key}')
            with open('puzzle_win.txt', 'a') as file:
                file.write(f"VELES | {caddr} | Wif: {wif2} | Key: {private_key}\n")
            stop_event.set()
            break
        else:
            count_dict['count'] += 1
            print(Fore.YELLOW + f'{count_dict["count"]} | Адрес: {caddr} | Key: {myhex}')
            
def main():
    print(Fore.YELLOW + """
██╗░░░██╗███████╗██╗░░░░░███████╗░██████╗░░░░░░██████╗░████████╗░█████╗░
██║░░░██║██╔════╝██║░░░░░██╔════╝██╔════╝░░░░░░██╔══██╗╚══██╔══╝██╔══██╗
╚██╗░██╔╝█████╗░░██║░░░░░█████╗░░╚█████╗░█████╗██████╦╝░░░██║░░░██║░░╚═╝
░╚████╔╝░██╔══╝░░██║░░░░░██╔══╝░░░╚═══██╗╚════╝██╔══██╗░░░██║░░░██║░░██╗
░░╚██╔╝░░███████╗███████╗███████╗██████╔╝░░░░░░██████╦╝░░░██║░░░╚█████╔╝
░░░╚═╝░░░╚══════╝╚══════╝╚══════╝╚═════╝░░░░░░░╚═════╝░░░░╚═╝░░░░╚════╝░                                     
      Программа предназначена только для расшифровки пазлов Сатоши,
                         используйте с умом ;)

          """)
    
if __name__ == '__main__':
    multiprocessing.freeze_support()
    colorama.init()
    main()
    puzl = int(input("Введите номер пазла: "))
    cores = int(input(Fore.YELLOW + f'Введите количество потоков для использования: '))
    y = 2**puzl
    x = 2**(puzl-1)
    
    chunk_size = (y - x) // cores
    jobs = []
    stop_event = multiprocessing.Event()
    for i in range(cores):
        start = x + i * chunk_size
        end = start + chunk_size
        p = multiprocessing.Process(target=seek, args=(start, end, stop_event))
        jobs.append(p)
        p.start()
    
    for job in jobs:
        job.join()

    input(Fore.YELLOW + f'Нажмите Enter для выхода...')

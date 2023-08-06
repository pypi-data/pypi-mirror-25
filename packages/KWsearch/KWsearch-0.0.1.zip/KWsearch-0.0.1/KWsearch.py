#-*- coding: utf-8 -*-
"""KWsearch v0.1 by Kopei Volodymyr (vkopey@gmail.com)
Програма призначена для швидкого пошуку в каталозі за ключовими словами.
Ключові слова вводяться в файлі class.pykb (кодування utf-8),
який розташований  цьому каталогі, і містить наприклад:
kw("книга", "book", "python")
Може працювати як плагін Total Commander.
Для цього перетягніть модуль на панель Total Commander і добавте параметр:
?%P -k або %P -k для додання ключових слів
?%P -i або %P -i для індексування поточного каталогу
?%P -s або %P -s для пошуку в поточному каталозі
Протестовано на Windows XP russian та Python 2.6"""

# Добавлено нечутливість до регістру букв
# Виправлено дублювання шляхів, які виводяться на вікно під час пошуку
# Добавлено режим редагування ключових слів
# Зробити можливість запуску коду бази в інтерпретаторі (execfile).
# Добавити меню

import os,sys
import Tkinter
import tkMessageBox
import pickle
import re

def makeCode(dr):
    """Повертає python код, згенерований за кореневим каталогом dr (unicode рядок)
    Додає в ключові слова також назву каталога і файлів каталогу"""
    # усі рядки повинні бути unicode !!!
    fileTypes=['.pdf','.djvu','.djv','.doc','.xls','.url','.txt']
    print "Please wait"
    KBcode=[]
    i=0 # для прогресу виконання обробки великих каталогів
    for root, dirs, files in os.walk(dr):
        KBcode.append(u'this=r"""'+root+'"""')#root.decode('mbcs')
        # додає тільки назви файлів заданого типу
        KBcode.append(u'files='+'['+u','.join(['"'+f+'"' for f in files if os.path.splitext(f)[1].lower() in fileTypes])+']')
        #KBcode.append(u'files=[]') # можна і без файлів
        if "class.pykb" in files: # якщо є файл class.pykb
            s=open(os.path.join(root,"class.pykb")).read() # прочитати його
            try:
                s=s.decode('utf-8') # намагатись конвертувати utf-8 в unicode
            except:
                s=u"kw()" # якщо не вийшло, то пустий список ключових слів 
            KBcode.append(s) # додати
        else: # якщо файлу class.pykb немає
            KBcode.append(u"kw()") # додати пустий список ключових слів
        i+=1
        if not i%1000: # кожні 1000 каталогів
            print i # виводити i
    print i," directories"
    # початок коду
    code1=u"""#-*- coding: utf-8 -*-
import os
def kw(*w):
    'Додає в список index ключові слова для даного каталога'
    index.append([this]+list(w)+files+[os.path.basename(this)])
"""    
    code=u"\n".join(KBcode)
    code=code1+code
    code=code.encode('utf-8')
    writeCode(code)
    return code

def writeCode(code):
    f=open('allKBcode.py','w')
    f.write(code)
    f.close()
    
def run(dr):
    """Будує базу індексів для каталогу dr (unicode рядок)"""
    ns={'index':index} # простір імен
    code=makeCode(dr) # отримати весь код
    exec(code, ns) # виконати код в просторі імен

def index2Unicode(index):
    return [[w.decode('utf-8') for w in r] for r in index]

def getIndexW(lst):
    """Повертає відсортований список елементів (для швидкого пошуку)
    [ключове слово, індекс каталогу]
    lst - список елементів [шлях каталогу, ключ. слово1, ключ. слово2,...]"""
    i=0 # поточний індекс lst
    indexW=[]
    for ws in lst: # для кожного елемента lst 
        for w in ws[1:]: # для кожного ключового слова
            indexW.append([w.lower(),i]) # добавити [ключове слово, індекс каталогу]
        i+=1
    return sorted(indexW) # відсортувати за ключовими словами
    
def loadIndex():
    """Завантажує індекси з файлів
    Повертає звичайний і відсортований списки ключових слів
    Якщо файл не існує, повертає [],[]"""
    fn=os.path.join(rootdir,'kwindex.pkl')
    if not os.path.isfile(fn): return [],[]
    f = open(fn, 'rb')
    index=pickle.load(f)
    indexW=pickle.load(f)
    f.close()
    return index,indexW 

def saveIndex():
    """Зберігає індекси у файли"""
    fn=os.path.join(rootdir,'kwindex.pkl')
    f = open(fn, 'wb')
    pickle.dump(index, f) # звичайний список
    pickle.dump(indexW, f) # відсортований список
    f.close()
    
def findSlice(lst,word):
    """Шукає індекси діапазону в відсортованому списку lst,
    в якому слова починаються з word. Для швидкого пошуку"""
    js=0 # індекс початку діапазону
    n=0 # кількість елементів в діапазоні
    i=0 # поточний індекс lst
    for w,k in lst: # для кожного елемента lst
        if w.startswith(word.lower()): # якщо w починається з word
            if n==0: # якщо до цього ще нічого не знайдено
                js=i # запам'ятати індекс початку діапазону
            n+=1 # збільшити кількість елементів в діапазоні
        elif n!=0: # інакше якщо було вже щось знайдено
            break # перервати
        i+=1
    return js,js+n

def find(lst,regex):
    """Повертає список елементів зі списку lst, які містять regex"""
    # ігнорує регістр букв
    po=re.compile(regex,re.IGNORECASE | re.UNICODE) # компілює шаблон в об'єкт регулярного виразу
    res=[] # список результатів
    for w,k in lst: # для кожного елемента lst
        mo=po.search(w)# знаходить у s першу відповідність шаблону
        if mo: # якщо знайдено
            res.append([w,k]) # добавити в список
    return res

#################################################################
#функції для додання ключових слів у файл class.pykb

def readKW(rootdir):
    """Повертає список ключових слів з файлу class.pykb"""
    fl=os.path.join(rootdir,"class.pykb") # шлях до class.pykb
    if not os.path.isfile(fl): # якщо немає такого файлу
        open(fl,'w').close() # створити пустий
        return []
    KWlst=[] # список ключових слів
    i,lns=findKWline(fl) # знайти номер рядка з ключовими словами
    if i==None: return [] # якщо немає рядка з ключовими словами
    ln=lns[i].rstrip() # рядок з ключовими словами
    for kw in ln[3:-1].split(","): 
        KWlst.append(kw.strip()[1:-1]) # додати ключове слово
    if KWlst==[""]: KWlst=[] # якщо містить пусте слово, то пустий список
    return KWlst

def findKWline(fl):
    """Повертає номер рядка з ключовими словами і список рядків"""
    f=open(fl,'r') # відкрити для читання
    lns=f.readlines() # список рядків
    f.close()
    for i,ln in enumerate(lns): # для кожного рядка
        ln=ln.rstrip() # без пробілів і '\n' вкінці
        if ln.startswith("kw(") and ln.endswith(")"): # якщо починається з "kw("
            return i,lns
    return None,lns # якщо не знайдено

def writeKW(rootdir, kw):
    """Записує список ключових слів у файл class.pykb"""
    fl=os.path.join(rootdir,"class.pykb") # шлях до class.pykb
    kw=['"'+w+'"' for w in kw] # додати лапки до кожного ключового слова
    newline="kw("+", ".join(kw)+")\n" # сформувати рядок з ключовими словами
    i,lns=findKWline(fl) # знайти номер рядка з ключовими словами
    if i==None: # якщо не знайдено
        lns=[newline]+lns # добавити як перший рядок
    else: # інакше
        lns[i]=newline # вставити замість рядка i
    f=open(fl,'w')
    f.writelines(lns) # зберегти
    f.close()
        
####################################################################
class MainWindow(Tkinter.Tk):
    '''Клас головного вікна програми GUI'''
    def __init__(self, kw=None):
        '''Конструктор. kw - список ключових слів'''
        Tkinter.Tk.__init__(self) #виклик конструктора базового класу
        sizex, sizey = self.wm_maxsize() #повернути max розмір
        sizex, sizey=sizex, sizey-60
        self.wm_geometry("%dx%d+0+0"%(sizex,sizey)) # установити розмір
        font = 'times 14 bold' # шрифт
        self.s1 = Tkinter.StringVar() # змінна для збереження тексту
        
        self.entry=Tkinter.Entry(self, textvariable=self.s1, font=font,) #width=sizex-4
        self.entry.pack(side='top', fill=Tkinter.X, pady=20)# розмістити
                
        self.frame2 = Tkinter.Frame(self) # фрейм з Listbox
        self.listbox = Tkinter.Listbox(self.frame2, selectmode=Tkinter.SINGLE,exportselection=0)
        scrollbar_y = Tkinter.Scrollbar(self.frame2)
        scrollbar_x = Tkinter.Scrollbar(self.frame2, orient=Tkinter.HORIZONTAL)
        scrollbar_y.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        scrollbar_x.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
        self.listbox.pack(side=Tkinter.TOP, fill=Tkinter.Y, expand=1)
        scrollbar_y['command'] = self.listbox.yview #scrollbar_y.config(command=listbox.yview)
        scrollbar_x['command'] = self.listbox.xview
        self.listbox['yscrollcommand'] = scrollbar_y.set 
        self.listbox['xscrollcommand'] = scrollbar_x.set
        self.listbox['width']=140
        self.frame2.pack(side=Tkinter.TOP, fill=Tkinter.Y, expand=1)
        
        if kw==None: # якщо режим пошуку
            self.title("KWsearch v0.1 - search mode") # заголовок
            self.entry.bind("<KeyRelease>", self.keyRelease)
            self.listbox.bind('<Double-ButtonRelease-1>', self.dblClicked1)
            self.totalcmd=r"c:\totalcmd\TOTALCMD.EXE" # шлях до Total Commander
            if not os.path.isfile(self.totalcmd): # якщо файлу не існує
                tkMessageBox._show('Warning',self.totalcmd+'\n - incorrect Total Commander path!',icon=tkMessageBox.WARNING,type=tkMessageBox.OK)
            # поточний список елементів [ключове слово, індекс каталогу]
            # потрібний для швидкого пошуку
            self.indexWcur=indexW
            
        else: # якщо режим додання ключових слів
            self.title("KWsearch v0.1 - add keyword mode") # заголовок
            self.entry.bind("<Return>", self.keyReturn)
            self.listbox.bind('<Double-ButtonRelease-1>', self.dblClicked2)
            self.kw=kw
            self.buildListKW()

#############################################################
# функції для режиму пошуку
   
    def buildList(self, lst):
        """Заповнює self.listbox елементами lst"""
        drs=set() # множина каталогів (для уникнення дублювань)
        for kw,i in lst: # для кожного у списку
            drs.add(index[i][0]) #добавити в множину назву каталогу
        for dr in drs:
            self.listbox.insert(Tkinter.END, dr) # добавити в список
                
    def keyRelease(self,event):
        """Відпускання клавіші під час набору тексту в entry
        Виводить результати відразу після натискання клавіш.
        Після натискання Enter виводить результати за регулярним виразом"""
        self.listbox.delete("0", Tkinter.END) # очистити список
        text= self.s1.get() # отримати текст з поля вводу
        if text=="":
            self.indexWcur=indexW
            return
        #http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
        if event.keysym=="Return": # якщо натиснуто Enter
            ind=find(indexW, text) # знайти за регулярним виразом
            self.buildList(ind) # вивести
            return        
        sl=findSlice(self.indexWcur,text) # знайти індекси діапазону
        if sl[1]!=0: # якщо щось знайдено
            self.indexWcur=self.indexWcur[sl[0]:sl[1]] # діапазон списоку елементів [ключове слово, індекс каталогу]
            self.buildList(self.indexWcur) # вивести
        
    def dblClicked1(self,event=None):
        """Подвійний натиск мишею. Відкриває каталог в Total Commander"""
        selIndex=self.listbox.curselection()[0] # індекс вибраного елементу
        path=self.listbox.get(selIndex) # текст вибраного елементу
        if os.path.isdir(path): # якщо каталог існує
            # відкрити його в totalcmd (який має бути запущений)
            os.system(self.totalcmd+' /O "'+path.encode('mbcs')+'"') # шлях в лапках!

#############################################################
# функції для режиму додавання ключових слів

    def keyReturn(self,event):
        """Натиск Enter. Додає нове ключове слово"""
        text= self.s1.get().encode('utf-8') # отримати текст з поля вводу
        if text and text not in self.kw: # перевірити корректність ключового слова
            self.kw.append(text) # добавити ключове слово
            writeKW(rootdir, self.kw) # записати ключові слова
            self.buildListKW() # перебудувати список
        
    def buildListKW(self):
        """Будовує список ключових слів"""
        self.listbox.delete("0", Tkinter.END) # очистити список
        for kw in self.kw: # для кожного ключового слова
            self.listbox.insert(Tkinter.END, kw) # добавити в список 

    def dblClicked2(self,event=None):
        """Подвійний натиск мишею. Видаляє ключове слово"""
        selIndex=self.listbox.curselection()[0] # індекс вибраного елементу
        text=self.listbox.get(selIndex) # текст вибраного елементу
        self.kw.remove(text.encode('utf-8')) # видалити ключове слово
        writeKW(rootdir, self.kw) # записати ключові слова
        self.buildListKW() # перебудувати список
        
##################################################################                          
# глобальні змінні
rootdir=None # кореневий каталог (unicode)       
index=[] # список unicode елементів [шлях каталогу, ключ. слово1, ключ. слово2,...]
indexW=[] # відсортований список елементів [ключове слово, індекс каталогу] 

if __name__ == '__main__':
    #sys.argv.append(ur"d:\!Music_unsaved") # !! для тестування
    #sys.argv.append('-k') # !! для тестування
    if len(sys.argv)==3: # якщо передані 2 аргументи через командний рядок
        rootdir=sys.argv[1] # задати кореневий каталог - перший аргумент командного рядка
        rootdir=rootdir.decode('mbcs') # конвертувати в unicode
        rootdir=rootdir[:-1] # забрати останный "\"
        if not os.path.isdir(rootdir): # якщо каталогу не існує
            print 'Incorrect path!'
            sys.exit() # вийти
        if sys.argv[2]=='-i': # якщо другий аргумент '-i' (індексація)
            run(rootdir) # створити індекси
            index=index2Unicode(index)
            indexW=getIndexW(index)
            saveIndex() # зберегти індекси
            print "Done!"
        if sys.argv[2]=='-s': # якщо другий аргумент '-s' (пошук)
            index,indexW=loadIndex() # завантажити індекси з файлу
            if index:
                root=MainWindow() # створити головне вікно
                root.mainloop() # головний цикл обробки подій
        if sys.argv[2]=='-k': # якщо другий аргумент '-k' (пошук)
            root=MainWindow(kw=readKW(rootdir)) # створити головне вікно
            root.mainloop() # головний цикл обробки подій
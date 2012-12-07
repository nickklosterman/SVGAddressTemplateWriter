#!/usr/bin/python

#http://www.gossamer-threads.com/lists/python/dev/662491
from __future__ import with_statement

class SVGTemplateWriter:
    def __init__(self,addressfile,svgtemplate,keyword):
        self.addressfile=addressfile
        self.svgtemplate=svgtemplate
        self.keyword=keyword
        self.addressList=[] #init all veriables before you try to use them....I had this declared after ExtractAddressList which uses it and so there was complaining that the class didn't have a self.addressList attribute
        self.templateList=[]
        self.incrementCounter=0    
        self.ExtractAddressList()
        #self.Temp()
        self.CompressList() #this is the simple lazy way to move through the list
#        self.CyclicSearchReplace()
        self.SplitTemplateFile()

    def ExtractAddressList(self):
#        print("using : %s" % self.addressfile)
        with open(self.addressfile,"r") as f:
            addresses = [elem for elem in f.read().split('\n') if elem]
            for address in addresses:
                temp=address.split(';')
                temp=[x.strip() for x in temp] #strip in lists http://stackoverflow.com/questions/7984169/using-strip-on-lists
                self.addressList.append(temp) #whitespace automatically stripped. This may not be the desired behavior for some people. They may try to pad the output using spaces.
        f.close()
#        print(self.addressList)

    def Temp(self):
        for item in self.addressList:
            for mini_item in item:
                print(mini_item)
    def CompressList(self): #list of lists into one list http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
        self.addressList=[item for sublist in self.addressList for item in sublist]
    def IncrementList(self):
        self.incrementCounter+=1
        listlength=len(self.addressList)
        if listlength>0:
            addressfieldlength=len(self.addressList[0])
                                   
    def SplitTemplateFile(self):
        templateFile = open(self.svgtemplate)
        tempoutput=''
        for line in templateFile:
            if self.keyword in line:
                firstHalf,secondHalf=line.split(self.keyword) #this assumes there is only one occurrence of the keyword per line
                tempoutput+=firstHalf
                self.templateList.append(tempoutput)
                tempoutput=secondHalf
            else:
                tempoutput+=line
        
        self.templateList.append(tempoutput)
        # for item in self.templateList:
        #     print(item)
        #     print("BREAK")
#        print(self.templateList)
        templateFile.close()

    def CyclicSearchReplace(self): #http://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
    #Create temp file
        counter=0
#        fh, abs_path = mkstemp() #http://docs.python.org/release/3.3.0/library/tempfile.html?highlight=mkstemp
 #       new_file = open(abs_path,'w')
        templateFile = open(self.svgtemplate)
        #substitution=self.addressList[0][0]

        for line in templateFile:
            if self.keyword in line:
                print(line.split(self.keyword))
                print(line,self.addressList[counter]) #,i=0 #increment the addresslistcounter
#                new_file.write(line.replace(self.keyword, subst))
                counter+=1             

            else:
                i=99
 #               new_file.write(line)
    #close temp file
  #      new_file.close()
#fh.close()#        close(fh)
        templateFile.close()
     #Move new file
        #move(abs_path, file)

        
    
import sys
import getopt


def main():
#    print(sys.argv[1:])
#pretty much straight from : http://docs.python.org/release/3.1.5/library/getopt.html
#took me a while to catch that for py3k that you don't need the leading -- for the long options
    try:
        options, remainder = getopt.gnu_getopt(sys.argv[1:], 'a:t:k:', ['addressfile=','svgtemplate=','keyword='])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

#Set default values for some variables. 
    keyword='TEXT'
    svgtemplate='template.svg'
    addressfile='addresslist.txt' #'addresses.txt'

    print(options)
    for opt, arg in options:
        if opt in ('-a', '--addressfile'):
            addressfile=arg
        elif opt in ('-k', '--keyword'):  #it took me the longest time to figure out why the Assert was always coming on. It was bc this was left an 'if' and not 'elif' so it was executing the first 'if' and then going through this 'if' and falling through and then exiting. That error sucked.  
            keyword=arg
        elif opt in ('-t', '--svgtemplate'):
            svgtemplate=arg
        else:
            print(opt,arg)
            assert False, "unhandled option"
            

    STW=SVGTemplateWriter(addressfile,svgtemplate,keyword)
#ExtractAddressList(addressfile)

if __name__=="__main__":
    main()

#Must avoid keyword being reserved word in SVG
#make sure no add'l spaces in your template, addresslist as this'll affect the balance of the layout. You may not notice it right away but you'll just feel that something is slightly off not knowing that an invisible space is throwing things off. 

#inkscape must be installed for (batch) printing which reqires exporting file to another format:http://unix.stackexchange.com/questions/11973/print-an-svg-from-the-command-line
# inkscape --without-gui --export-pdf=foo.pdf foo.svg
# lpr foo.pdf
# Or if you want to print directly:
# inkscape --without-gui --export-pdf=/dev/stdout foo.svg | lpr




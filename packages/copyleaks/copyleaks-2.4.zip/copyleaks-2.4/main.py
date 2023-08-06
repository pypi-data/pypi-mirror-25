'''
 The MIT License(MIT)
 
 Copyright(c) 2016 Copyleaks LTD (https://copyleaks.com)
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''

import time
import sys
dirPath = './copyleaks'
if dirPath not in sys.path:
    sys.path.insert(0, dirPath)

from copyleakscloud import CopyleaksCloud
from processoptions import ProcessOptions
from product import Product


if __name__ == '__main__':
    #edit your login credentials.
    cloud = CopyleaksCloud(Product.Businesses, '<YOUR_EMAIL_HERE>', '<YOUR_API_KEY_HERE>')
    
    print("You've got %s Copyleaks %s API credits" % (cloud.getCredits(), cloud.getProduct())) #get credit balance
    
    options = ProcessOptions()
    options.setSandboxMode(True) # In production, comment this line (skip sandbox mode).

    print("Submitting a scan request...")
    
    process = cloud.createByUrl('https://copyleaks.com', options)
    #process = cloud.createByOcr('ocr-example.jpg', eOcrLanguage.English, options)
    #process = cloud.createByFile('test.txt', options)
    #process = cloud.createByText("Lorem ipsum torquent placerat quisque rutrum tempor lacinia aliquam habitant ligula arcu faucibus gravida, aenean orci lacinia mattis purus consectetur conubia mauris amet nibh consequat turpis dictumst hac ut nullam sodales nunc aenean pharetra, aenean ut sagittis leo massa nisi duis nullam iaculis, nulla ultrices consectetur facilisis curabitur scelerisque quisque primis elit sagittis dictum felis ornare class porta rhoncus lobortis donec praesent curabitur cubilia nec eleifend fringilla fusce vivamus elementum semper nisi conubia dolor, eros habitant nisl suspendisse venenatis interdum nulla interdum, libero urna maecenas potenti nam habitant aliquam donec class sem hendrerit tempus.")
    #processes, errors = cloud.createByFiles(['path/to/file1', 'path/to/file2'], options)
    
    print ("Submitted. In progress...")
    iscompleted = False
    while not iscompleted:
        [iscompleted, percents] = process.isCompleted() #get process status
        print ('%s%%' % (percents))
        if not iscompleted:
            time.sleep(3)
    
    print ("Finished!")
    
    results = process.getResutls() #get scan results
    print ('\nFound %s results...' % (len(results)))
    for result in results:
        print('')
        print('------------------------------------------------')
        print('Title: %s' % (result.getTitle()))
        print('Introduction: %s' % (result.getIntroduction()))
        print ("Information: %s copied words (%s%%)" % (result.getNumberOfCopiedWords(), result.getPercents()))
        print ('URL: %s' % (result.getUrl()))
        print ('Comparison link: %s' % (result.getEmbededComparison()))
        
        # Optional: Download result full text. Uncomment to activate
        #print ("Result full-text:")
        #print("*****************")
        #print(process.getResultText(result))
        
        # Optional: Download comparison report. Uncomment to activate
        #print ("Comparison report:")
        #print("**************")
        #print (process.getResultComparison(result))
    
    # Optional: Download source full text. Uncomment to activate.
    #print ("Source full-text:")
    #print("*****************")
    #print(process.getSourceText())
    pass



def run():# Import the required libraries
    import webview

    # Create a GUI window to view the HTML content
    with open("fl")as fl:
        firstlaunchhtml = fl.read()
    open("fl","w+").close()      
    webview.create_window('Welcome!' ,html=firstlaunchhtml)
    open('fl', "w+").close()
    webview.start()
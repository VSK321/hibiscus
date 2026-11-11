# Hibiscus

A proof of concept implementation of a Python focused single-page server-side web framework that was inspired by .NET's Blazor. 

THIS IS ONLY A PROOF OF CONCEPT! DO NOT USE THIS IN ANY LIVE APPLICATIONS! Look at the compiler file/all method naming conventions if you want to see why it would be a terrible idea.

## Example Application

To test the example application, ensure the hibiscus folder is in your PATH and run main.py. 

## Functionality

While the labels all imply the framework is akin to an MVC style structure, it is quite different. 

All files within the current directory are considered to be a part of the application. To exclude a file, type "#ignore" in the first line. Why did I do this? Django's system of including each file explicitly was quite frustrating to me so this felt smoother. However, there are many arguments (perticularly from the security aspect) to not do this. The only requirement is to have a "shared" folder which is just for the App and MainLayout "views". The main layout is static and any js/css files can be added here. 

### "Views"

Each "view" is made up of a PAGE_NAME.py and a PAGE_NAME.hibiscus file. In the background, the .hibiscus file is converted to a python file and imported as a partial class to attach onto the main view class in the PAGE_NAME.py file. Due to this, all class variables are shared between the two files. The route to the page is set via the "app" object with any number of parameters as shown in Counter.py. This structure was inspired by django's system albeit there can only be one class per file. 

Within the .hibiscus file, to call a variable, do "~(self.variable)~". If you want to attach a "call" to a Python function, use the usual event preceeded with hbs (e.g. "oninput" becomes "hbsinput"). This just attaches an event listener on the client side and, if the appropriate interaction occurs, the websocket controller (hibsicusWS.py) is called which, in turn, call the function, updates the page and sends the change in the page over to the client. You can also include variables to pass to a PAGE_NAME.py function by including the hbsid tag (Counter.hibiscus does this to add the number to itself). However, note that when using hbsid, the variable is always returned as a string so you cannot pass just any object yet. 

One question could be, what if I want to update the client page when a change occurs on the server-side? In theory it should be possible to do so as an update to the client is not linked to a request being sent. However, this would likely be a next step. 

Another popular idea is probably calling a view within a view. This can be done as shown in the App.hibiscus/.py. NavMenu is called by first creating an instance of the class within the .py file and, in the hibiscus file, call via "~(await self.menu.main())~". 

### "Controllers"

This term is technically correct! Given that this framework does support jinja2, you can create a controller that returns a real view. To do this, within the main function of the controller, await self.return_page(FILE_PATH, PARAMS). Besides that, the format is similar to that of the PAGE_NAME.py view above. 

## Next Steps

Probably a good idea to update the naming convention. This project is currently the culmination of approx. 5 years of on and off development with many rewrites. 

Direct server-side updates would also be quite a useful next step. 

Given that Django now supports ASGI, it could be interesting to see if the project can act as an extension rather than a worse alternative. 

It would be good to create some proper documentation. 

The "compiler" is also quite poorly written so updating it would be useful. 

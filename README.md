## london-comments app for London framework

### How to use it:

- install it 
- add it to INSTALLED_APPS

    INSTALLED_APPS = {
        ...
        'comments': 'comments'
    }

- add it to TEMPLATE_CONTEXT_PROCESSORS

	TEMPLATE_CONTEXT_PROCESSORS = (
	        ...
	        'comments.context_processors.basic',
	        )
	        
- add MODELS_WITH_COMMENTS to *settings.py*
	        
	       
	#dict in {'model': 'app'} format
	MODELS_WITH_COMMENTS = {
	                        'Profile': 'profiles',
	                        'Page': 'pages',
	                        }
	                        
- add it to template as

	{{ render_comments_for(obj) }}
	
That's all!
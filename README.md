## london-comments app for London framework

### How to use it:

1. Install it 
2. Add it to INSTALLED_APPS

    INSTALLED_APPS = {
    ...
    'comments': 'comments'
    }

3. Add it to TEMPLATE_CONTEXT_PROCESSORS

	TEMPLATE_CONTEXT_PROCESSORS = (
	        ...
	        'comments.context_processors.basic',
	        )
	        
4. Add MODELS_WITH_COMMENTS to *settings.py* like dict in *{'model': 'app'}* format
	        
    MODELS_WITH_COMMENTS = {
    					'Profile': 'profiles',
    					'Page': 'pages',
    }
	                        
5. Add it to template as

	{{ render_comments_for(obj) }}
	
That's all!
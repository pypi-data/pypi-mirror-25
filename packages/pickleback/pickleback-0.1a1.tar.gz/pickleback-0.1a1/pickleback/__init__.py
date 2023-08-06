def register():
    from matplotlib.backend_bases import register_backend
    for ext in ['pkl', 'pickle']:
        register_backend(ext, 'pickleback.backend_pkl',
                         'Python pickle format, to be used with caution on a '
                         'single matplotlib version')

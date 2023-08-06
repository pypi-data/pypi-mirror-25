from atelier.invlib.ns import ns
ns.setup_from_tasks(
    globals(), "lino_xl",
    languages="en de fr et nl pt-br es".split(),
    tolerate_sphinx_warnings=False,
    blogref_url='http://luc.lino-framework.org',
    revision_control_system = 'git',
    locale_dir='lino_xl/lib/xl/locale',
    doc_trees= [])
                    


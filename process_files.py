import pandas as pd
import magic

files_dir = 'data/'
doc_descr = 'appl_doc_files.xlsx'
doc_false_descr = 'appl_doc_false_files.xlsx'

doc_df = pd.read_excel(doc_descr)
doc_false_df = pd.read_excel(doc_false_descr)

doc_df = doc_df[['link', 'files', 'path']]
doc_df = doc_df.dropna()
doc_df = doc_df.loc[~doc_df['path'].str.contains('Exception')]

doc_false_df = doc_false_df[['link', 'files', 'path']]
doc_false_df = doc_false_df.dropna()
doc_false_df = doc_false_df.loc[~doc_false_df['path'].str.contains('Exception')]


def get_filetype(filepath):
    mime = magic.Magic(mime=True)
    return mime.from_file(filepath)


def apply_filetype(row):
    current_list = eval(row)
    return_list = []
    for path in current_list:
        return_list.append(get_filetype(path))
    return return_list


# doc_df['filetypes'] = doc_df['path'].apply(apply_filetype)
# doc_df.to_excel('doc_descr.xlsx')

doc_false_df['filetypes'] = doc_false_df['path'].apply(apply_filetype)
doc_false_df.to_excel('doc_false_descr.xlsx')
from crawler.pubmed_api import excute_pubmed_api
import time
import os
# Set the Entrez Utilities base URL
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
my_api_key = "27af1ec10cd5d499b43225ebf7f669d90b09"
# Set the query parameters
db = "pubmed"
retmax = 20
def add_BX_tag(lst_text):
    return [(item,'B-X') for item in lst_text]

source_file_path = r'datasets/MTL-Bioinformatics-2016/BC5CDR-chem-IOBES/test.tsv'
with open(source_file_path,'r') as f:
    text = f.read()

folder_path =r'datasets/MTL-Bioinformatics-2016-external-contexts'
folder_name = source_file_path.split('/')[-2]+'_eos_doc_full'

fi_name = source_file_path.split('/')[-1]
if fi_name.split('.')[0]=='devel':
    fi_name = 'dev.'+source_file_path.split('/')[-1].split('.')[1] 

# Combine the path and folder name into a single string
new_folder = os.path.join(folder_path, folder_name)
if not os.path.exists(new_folder):
    os.mkdir(new_folder)


start = 1 

sublists = text.strip().split('\n\n')[count-1:]
result = []
queries = []
count = 0
non_exten_count = 0
print("Nếu như request lỗi thì setting lại start bằng chính số log ra cuối cùng ở màn hình console! Nếu như có nhiều lần lỗi thì cộng tiếp vào")
for sublist in sublists:
    if sublist != '':
        count+=1
        print(count)
        tokens = sublist.split('\n')
        sublist_result = []
        text_ = ""
        for token in tokens:
            text_+= (token.split('\t')[0]) + " "
            sublist_result.append((token.split('\t')[0], token.split('\t')[1]))
        query = text_.strip()
        external_tokens = excute_pubmed_api(base_url=base_url,api_key=my_api_key,db=db,retmax=retmax,query=query)
        if len(external_tokens)==0:
            non_exten_count+=1
            result.append(sublist_result)
        else:
            external_context = add_BX_tag(['<EOS>']+external_tokens)
            sublist_result.extend(external_context)
            result.append(sublist_result)

        to_file= ('\n'.join([t[0] + '\t' + t[1] for t in sublist_result]) + '\n\n')
        with open(new_folder+"/"+fi_name,'a', encoding='utf-8') as f:
            f.write(to_file)
    time.sleep(0.16)

print(non_exten_count)
to_file = ""
for sub_list in result:
    to_file= to_file + ('\n'.join([t[0] + '\t' + t[1] for t in sub_list]) + '\n\n')
with open(new_folder+"/"+fi_name+"_FULL",'a', encoding='utf-8') as f:
    f.write(to_file)



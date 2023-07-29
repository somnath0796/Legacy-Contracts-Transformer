import json
import os
from PIL import Image


def generate_samples(dir_path='.'):

    files = os.listdir(dir_path)

    if len(files) != 0:
        imgs = [f for f in files if f.endswith('jpg')]
        json_s = [f for f in files if f.endswith('json')]
        # print(files)
        # print(imgs)
        # print(json_s)

        assert len(imgs) == len(json_s)
        # print('required files present')

        for i in imgs:
            path = os.path.join(dir_path, i[:-4])

            if not os.path.exists(path):
                os.mkdir(path)
            json_path = os.path.join(dir_path, i[:-4]+'.json')

            # creation of gt
            with open(os.path.join(dir_path,'legacy_gt.txt'), 'a') as fd:
                with open(json_path, 'rb') as file:

                    j = json.load(file)
                    img = Image.open(os.path.join(dir_path, i)).convert('RGB')
                    # img.show()
                    base_name = i[:-4]
                    itr = 0
                    for seg in j['shapes']:
                        seg_name = base_name + '-' + str(itr)
                        seg_label = seg['label']
                        seg_bb = [y for x in seg['points'] for y in x]
                        try:
                            seg_img = img.crop(tuple(seg_bb))
                        except:
                            print(seg_bb, seg_label, seg_name)

                        seg_save_path = os.path.join(dir_path, base_name, seg_name+'.jpg')
                        
                        if not os.path.isfile(seg_save_path):
                            seg_img.save(seg_save_path)

                        gt_text = os.path.join(base_name, seg_name+'.jpg') + " " + seg_label + " |*| " + " ".join(str(e) for e in seg_bb)
                        
                        fd.write(gt_text+'\n')

                        itr += 1
                file.close()
            fd.close()

def gt_without_bb(dir_path="."):
    with open(os.path.join(dir_path,'legacy_gt.txt'), 'r') as f:
        gts = f.readlines()
    f.close()
    
    
    fixed_gts = [(text.split(' |*| ')[0]) for text in gts]

    with open(os.path.join(dir_path,'legacy_gt_no_bb.txt'), 'w') as f1:
        for gt in fixed_gts:
            f1.write(gt+'\n')
    f1.close()
    pass

    # for json_file in
if __name__ == '__main__':
    #generate_samples('test contracts')
    gt_without_bb('test contracts')

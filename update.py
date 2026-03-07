import json,pickle,os,time,datetime
from Configuration import _DEFAULT_CONFIGURATION
from post_processing.stat_accumu import StatFlowDataset,StatFrame,_MISSING_NO_STATIC_FRAME
from post_processing.stat_json import from_statflow, from_refmap_entry, _MISSING_NO_READABLE, as_readable


def fetch_dataset() -> StatFlowDataset:
    with open(file=config.pth_to_raw_dataset, mode="rb") as raw_dataset:
        latest: StatFlowDataset = pickle.load(raw_dataset)
    return latest

config = _DEFAULT_CONFIGURATION
dataset = fetch_dataset()
with open(config.pth_to_refmap, 'r') as f:
    refmap: dict[str, dict] = json.loads(f.read())

def get_ids() -> list[str]:
    global config,dataset
    return list(dataset.dataset.keys())

ids = get_ids()

def get_stat_by_id(idd: str) -> list[StatFrame]:
    global config,dataset
    idd = idd.lower()
    if idd in get_ids():
        return dataset.dataset[idd]
    print(f"warn-No such id: {idd}")
    return [_MISSING_NO_STATIC_FRAME]

def update_all_preprints():
    global config,ids
    for idx,idd in enumerate(ids):
        os.system("cls")
        print(f"updating preprint: {idd}, {idx+1}/{len(ids)} ({(idx/len(ids))*100}%)")
        statflow: list[StatFrame]=get_stat_by_id(idd)
        with open(file=os.path.join(config.pth_to_endpoint_root,"data",idd+".json"), mode="w") as target_file:
            json.dump(from_statflow(statflow), target_file)

def update_metainf():
    global config,ids,refmap

    for idx,idd in enumerate(ids):
        os.system("cls")
        print(f"updating metainfo: {idd}, {idx + 1}/{len(ids)} ({(idx / len(ids)) * 100}%)")
        if idd in refmap:
            entry = refmap[idd]
            with open(file=os.path.join(config.pth_to_endpoint_root,"meta",idd+".json"), mode="w") as target_file:
                json.dump(from_refmap_entry(entry), target_file)

def update_readable_id_map():
    global config,ids,refmap
    readable_map: dict[str, str] = {}
    for idx,idd in enumerate(ids):
        try:
            future = {as_readable(refmap[idd]): idd}
        except KeyError:
            print(f"warn-No such id in refmap: {idd}")
            future = {_MISSING_NO_READABLE: idd}

        readable_map.update(future)

    with open(file=os.path.join(config.pth_to_endpoint_root, "readable.json"), mode="w") as target_file:
        json.dump(readable_map, target_file)

def push_to_github():
    global config
    commit_message = f"Auto update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    return os.system(config.pth_to_pusher_batch_abs + " \"" + commit_message + '\"')

def update_all():
    try:
        update_all_preprints()
        update_metainf()
        update_readable_id_map()
        time.sleep(2) # await for filesystem resource release
        push_to_github()
        return True
    except Exception as ignored:
        print(ignored)
        return False

if __name__ == "__main__":
    update_readable_id_map()
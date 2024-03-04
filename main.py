from nbt import nbt
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap


def nbt_to_dict(tag, yaml_map=None):
    """
    NBT 태그를 Python 딕셔너리로 변환합니다. 배열 타입의 길이와 타입 정보를 주석으로 처리합니다.
    """
    if yaml_map is None:
        yaml_map = CommentedMap()

    if isinstance(
        tag,
        (
            nbt.TAG_String,
            nbt.TAG_Float,
            nbt.TAG_Double,
            nbt.TAG_Byte,
            nbt.TAG_Short,
            nbt.TAG_Int,
            nbt.TAG_Long,
        ),
    ):
        # 기본 타입은 값만 반환
        return tag.value
    elif isinstance(tag, (nbt.TAG_Int_Array, nbt.TAG_Byte_Array, nbt.TAG_Long_Array)):
        # 배열 타입의 경우, 길이 정보를 주석으로 추가
        values = [t.value for t in tag]
        yaml_map.yaml_add_eol_comment(f"Array length: {len(tag)}", len(yaml_map))
        return values
    elif isinstance(tag, nbt.TAG_List):
        list_values = [nbt_to_dict(t) for t in tag]
        return list_values
    elif isinstance(tag, nbt.TAG_Compound):
        for t in tag.values():
            yaml_map[t.name] = nbt_to_dict(t, CommentedMap())
        return yaml_map
    else:
        raise ValueError(f"Unsupported NBT tag type: {type(tag)}")


def save_as_yaml(data, filename):
    """
    데이터와 주석을 포함하여 YAML 파일로 저장합니다.
    """
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    with open(filename, "w") as outfile:
        yaml.dump(data, outfile)


if __name__ == "__main__":
    # NBT 파일 로드
    nbtfile = nbt.NBTFile("dirtfarm.nbt", "rb")

    # NBT 데이터를 Python 딕셔너리로 변환
    data = nbt_to_dict(nbtfile)

    # 변환된 데이터를 YAML 파일로 저장
    save_as_yaml(data, "dirtfarm.nbt.yaml")

    print("NBT to YAML conversion completed. Check output.yaml.")

from nbt import nbt

# place the generated nbt file in
# saves/worldname/generated/minecraft/structures/your_structure.nbt
# and run the following command in the game
# /place template minecraft:your_structure
# then you can use the structure block to place the structure


def make_structure_nbt(structure, palette):
    nbtfile = nbt.NBTFile()
    nbtfile.name = "root"

    # DataVersion, 필요에 따라 수정하세요.
    nbtfile.tags.append(nbt.TAG_Int(name="DataVersion", value=2584))

    # 구조물의 크기 계산
    height = len(structure)
    length = len(structure[0].split("\n"))
    width = max(len(line) for layer in structure for line in layer.split("\n"))
    nbtfile.tags.append(nbt.TAG_List(name="size", type=nbt.TAG_Int))
    nbtfile["size"].tags.extend(
        [nbt.TAG_Int(width), nbt.TAG_Int(height), nbt.TAG_Int(length)]
    )

    # 팔레트 생성
    palette_list = nbt.TAG_List(name="palette", type=nbt.TAG_Compound)
    block_state_indices = {}
    for symbol, block_id in palette.items():
        block_state = nbt.TAG_Compound()
        block_state.tags.append(nbt.TAG_String(name="Name", value=block_id))
        palette_list.tags.append(block_state)
        block_state_indices[symbol] = len(palette_list) - 1
    nbtfile.tags.append(palette_list)

    # 블록 목록 생성
    blocks_list = nbt.TAG_List(name="blocks", type=nbt.TAG_Compound)
    for y, layer in enumerate(structure):
        for z, line in enumerate(layer.split("\n")):
            for x, symbol in enumerate(line):
                if symbol in block_state_indices:
                    block = nbt.TAG_Compound()
                    block.tags.append(
                        nbt.TAG_Int(name="state", value=block_state_indices[symbol])
                    )
                    block.tags.append(nbt.TAG_List(name="pos", type=nbt.TAG_Int))
                    block["pos"].tags.extend(
                        [nbt.TAG_Int(x), nbt.TAG_Int(y), nbt.TAG_Int(z)]
                    )
                    blocks_list.tags.append(block)
    nbtfile.tags.append(blocks_list)

    # entities 태그 추가 (이 예제에는 엔티티 없음)
    nbtfile.tags.append(nbt.TAG_List(name="entities", type=nbt.TAG_Compound))

    return nbtfile


if __name__ == "__main__":
    # 사용 예
    structure_nbt = make_structure_nbt(
        structure=["@@@@####@@@@\n@@@@####@@@@", "@@@@####@@@@\n@@@@####@@@@"],
        palette={
            "@": "minecraft:stone",
            "#": "minecraft:air",
        },
    )

    # 파일로 저장
    structure_nbt.write_file("example_structure.nbt")

import collections
import math

def find_repeats(text, min_len=3, max_len=10):
    """
    找出密文中重复的字段及其位置和距离
    """
    # 清洗文本，移除空格和换行
    text = "".join(text.split()).lower()
    results = {}

    print(f"{'重复字段':<15} | {'出现次数':<8} | {'出现位置':<20} | {'间距 (Distances)'}")
    print("-" * 70)

    for length in range(max_len, min_len - 1, -1):
        for i in range(len(text) - length):
            seq = text[i:i+length]
            # 找该序列在全文中出现的所有位置
            positions = []
            idx = text.find(seq)
            while idx != -1:
                positions.append(idx)
                idx = text.find(seq, idx + 1)
            
            # 如果出现次数大于1，且还没被记录过（长序列包含了短序列的情况）
            if len(positions) > 1 and seq not in results:
                # 检查这个序列是否是已知长序列的子集（去重）
                is_sub = False
                for already_found in results:
                    if seq in already_found:
                        is_sub = True
                        break
                
                if not is_sub:
                    results[seq] = positions
                    # 计算间距
                    distances = [positions[j] - positions[j-1] for j in range(1, len(positions))]
                    pos_str = ", ".join(map(str, positions))
                    dist_str = ", ".join(map(str, distances))
                    print(f"{seq:<15} | {len(positions):<8} | {pos_str:<20} | {dist_str}")

    return results

def get_gcd_list(distances):
    """
    计算一组距离的公约数（可选辅助功能）
    """
    if not distances: return None
    # 扁平化所有间距列表
    flat_distances = [d for sublist in distances for d in sublist]
    return flat_distances

# --- 使用方法 ---
# 将你的序号6密文粘贴在这里
ciphertext = """
cjtsbbczihewzdcfcazcznlaovjkmtxhgicszbixgjkidmizsbrbfcgfjlffkinbtpeqqbizwuzjqzmu
vfactvpapuviyihzyhjczmircnicgxirjbeumzcmphervmquuozbfmfxgjkimtmfqljqmxyfqaysgvcf
gkjhmbyehyfafpyfwydcutirgbicbmntguvkxgqqfcfbzmoycuekubbtkznwrmgmtpvhfmeaxljwmzlu
xluwzbbqwuzhqlmfcavguvzansfkuvamalrfmauswljhxmwfwyvftmqmuhgdaqhfgkkcfpyrcjlzfguf
cnvvqjyoctvhtmsawuxsebjdqmvgewlmvaysuvmfkalhqnidckmozkypualrkqhfjljqtwixqmdofpyy
cazqeebqtlysiimrtlhiqvnxatzgfieqpmffmolmfbrhqangflehuvntgsvumksahqfvzdizpllamvhb
tvtsqlczizfteggbqzzouvjgtldofpyycazqeigqtptozuufjldofqwmnzfqumnkxvciymcethvztifb
gyzbbzirgzjcdmgqtpkiewzycaysyinuezrhfpygppmsdacfavwhazizvvisoifxgkkvquufjldofqwe
gumwdwhygukcrxlupjvhavufvozgfqgqfbiwzontgyvkqzymvwiwzkyfquraavaavovfebbqryftqama
tzvwemhtcykzqnmojlknimxpgysidvwtwytvtxladlihewhiknesdjiojuvfiqfwualqwmlnqoeszjfg
uamsntyzxvebqcgmpurzqfuzflikqgfqkujhqqhmpkrgfzymovwjuacfqyjoywhsvovaywhfivdsdgvd
cbvfowrqvliupmfngyeokaoxctrznmlffpiooxugnpaseayzofvfehcbrpebmsukctrhqlgmtazbxmpu
pzfbnmlsohewznyxfjyoniofahernwoomhvffqhfjpjumtujavwgfilexvebqcgmpuiopqufgkvloqnq
olehtqmxgjkidmmapozznmlfuwrqquymubisfpyatfiwzomahvgsdinatztoxtyppvnjavhqwtrbzifs
giioeihpevehuvoawzxsauyftfwoekczcavrmtudilripqyzelrhfpypcpcmmnnqtufczbymjlvbsiaq
fzfaqqhmovjhxqpqnfrbpanuobcofqhsfpjqgamuqunwfpinxpfielyxknyhtmyjrsrwzmxonhiwrqyp
cuuozifkbluddwvxgtjczbbquwfhmvxsccvvqtjfqvesmvxmnswsxtiiohkvquufkjzozauzfwymeqwu
uajamzpqnluofbbquwvspecfjdywoppapuviyihzevlzpihmnfqsmvxeqsmsowgbnloddwvxgtjaaany
caysyinueprbexlaxlnvmbntgftozdizpllamvhbtvmseebmvovkmvneyhjobwjgnhigmgczihdczogm
vovambcokheganbuukrm
"""

print("Kasiski 分析结果：\n")
repeats = find_repeats(ciphertext)
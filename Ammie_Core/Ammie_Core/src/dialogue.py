import json
import os
from .llm_bridge import LLMBridge

class AmmieDialogueEngine:
    def __init__(self, root="configs"):
        """
        初始化引擎
        :param root: 配置文件所在的根目录
        """
        self.root = root
        self.llm = LLMBridge()
        self.scene = {"WHO": "user", "WHAT": "IDLE", "WHEN": "now", "WHERE": "virtual"}
        self.load_configs()

    def load_configs(self):
        """从 root 目录加载所有 JSON 配置文件"""
        # 使用 os.path.join 确保跨平台路径兼容性
        paths = {
            "symbols": os.path.join(self.root, "symbols.json"),
            "scenes": os.path.join(self.root, "scenes.json"),
            "ontology": os.path.join(self.root, "ontology.json"),
            "capabilities": os.path.join(self.root, "capabilities.json")
        }
        
        with open(paths["symbols"], 'r', encoding='utf-8') as f: self.symbols = json.load(f)
        with open(paths["scenes"], 'r', encoding='utf-8') as f: self.scenes = json.load(f)
        with open(paths["ontology"], 'r', encoding='utf-8') as f: self.ontology = json.load(f)
        with open(paths["capabilities"], 'r', encoding='utf-8') as f: self.capabilities = json.load(f)

    def save_configs(self):
        """将更新后的符号表持久化到本地"""
        path = os.path.join(self.root, "symbols.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.symbols, f, ensure_ascii=False, indent=2)

    def update_scene(self, user_input):
        """简单的 4W 场景感知逻辑"""
        if any(w in user_input for w in ["家", "回"]): 
            self.scene["WHERE"] = "home"
        elif any(w in user_input for w in ["公司", "办公室"]): 
            self.scene["WHERE"] = "office"

    def check_ontology(self, subject_atom, action_atom):
        """本体论合法性检查：判断主体是否有权执行该动作"""
        entity_map = {"REF_SELF": "ammie", "REF_USER": "user"}
        ent_name = entity_map.get(subject_atom)
        act_name = action_atom.lower().replace("action_", "")
        allowed = self.ontology.get("entities", {}).get(ent_name, {}).get("actions", [])
        return act_name in allowed

    def evolve(self, user_input):
        """演化机制：当识别到未知动作时，咨询 LLM 并更新符号表"""
        print(f"DEBUG: 识别到未知意图，尝试演化语义...")
        learn_prompt = (
            f"解析输入: '{user_input}'。提取其中的动作词。仅返回 JSON。格式：\n"
            "{\"new_atom\": \"动词(如:说谎)\", \"canonical\": \"ACTION_XXX\", \"intent\": \"QUERY_XXX\"}"
        )
        evolution_data = self.llm.ask(learn_prompt)
        
        if "intent" in evolution_data:
            atom = evolution_data.get("new_atom")
            canon = evolution_data.get("canonical")
            if atom and canon:
                # 写入原子词映射
                if "atomic" not in self.symbols: self.symbols["atomic"] = {}
                self.symbols["atomic"][atom] = {"canonical": canon}
                
                # 构建逻辑映射
                required = [canon]
                if "你" in user_input: required.append("REF_SELF")
                if "logic_map" not in self.symbols: self.symbols["logic_map"] = []
                self.symbols["logic_map"].append({"required": required, "intent": evolution_data["intent"]})
                
                self.save_configs()
                self.load_configs()
                return "【学习成功】已掌握新词汇，请再次提问。"
        return "无法理解该动作。"

    def process_input(self, user_input):
        """核心处理流程：解析 -> 本体检查 -> 意图匹配"""
        self.update_scene(user_input)
        
        # 1. 符号解析
        found_atoms = []
        atom_to_raw = {}
        for word, info in self.symbols.get("atomic", {}).items():
            if word in user_input or any(alias in user_input for alias in info.get("aliases", [])):
                canon = info["canonical"]
                found_atoms.append(canon)
                atom_to_raw[canon] = word

        # 2. 本体论拒绝机制（自主解释构建）
        if "REF_SELF" in found_atoms:
            actions = [a for a in found_atoms if a.startswith("ACTION_")]
            for act in actions:
                if not self.check_ontology("REF_SELF", act):
                    raw_word = atom_to_raw.get(act, "这个")
                    vocab = self.symbols.get("response_components", {}).get("VOCABULARY", {})
                    # 基于 S-V-O 结构自主拼装回复
                    return f"[{self.scene['WHERE']}] {vocab.get('REF_SELF','我')}{vocab.get('NEGATIVE','不会')}{raw_word} ✨"

        # 3. 意图逻辑匹配
        for rule in self.symbols.get("logic_map", []):
            if all(atom in found_atoms for atom in rule["required"]):
                return f"[{self.scene['WHERE']}] 好的，我这就处理。 ✨"

        # 4. 若无法处理，进入演化阶段
        return self.evolve(user_input)
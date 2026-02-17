import sys
import os
# 确保可以导入 src 目录下的模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.dialogue import AmmieDialogueEngine

def start_ammie():
    # 路径指向存储 JSON 文件的 configs 文件夹
    # 确保你已经创建了该文件夹并将 6 个 JSON 放入其中
    config_path = os.path.join(os.path.dirname(__file__), "configs")
    
    try:
        engine = AmmieDialogueEngine(root=config_path)
    except FileNotFoundError as e:
        print(f"错误：找不到配置文件。请确保 '{config_path}' 目录及其 JSON 文件存在。")
        return

    print("--- Ammie Core v0.1.3 (Atomic Fix) 已启动 ---")
    print("输入 'exit' 或 'quit' 退出。")
    
    while True:
        try:
            user_text = input("\nUser: ").strip()
            if not user_text: continue
            if user_text.lower() in ["exit", "quit"]: break
            
            # 运行核心因果链
            response = engine.process_input(user_text)
            print(f"Ammie: {response}")
            
        except (KeyboardInterrupt, EOFError):
            print("\n再见。")
            break
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    start_ammie()
class DiagramTool:
    @staticmethod
    def wrap_mermaid(diagram: str) -> str:
        return f"```mermaid\n{diagram.strip()}\n```"

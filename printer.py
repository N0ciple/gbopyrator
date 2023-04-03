from rich.console import Console


class Printer(Console):
    def __init__(self, quiet=False):
        super().__init__(width=80)
        self.quiet = quiet

    def print(self, *args, **kwargs):
        if not self.quiet:
            super().print(*args, **kwargs)

    def greetings(self):
        if not self.quiet:
            self.print(
                """[bold blue_violet]
            __________     ____                         __            
           / ____/ __ )   / __ \____  __  ___________ _/ /_____  _____
          / / __/ __  |  / / / / __ \/ / / / ___/ __ `/ __/ __ \/ ___/
         / /_/ / /_/ /  / /_/ / /_/ / /_/ / /  / /_/ / /_/ /_/ / /    
         \____/_____/   \____/ .___/\__, /_/   \__,_/\__/\____/_/     
                            /_/    /____/                             
            [/bold blue_violet]"""
            )

    def warning(self, message):
        if not self.quiet:
            self.print(f"[bold orange1]⚠️ {message}[/bold orange1]")

    def error(self, message):
        if not self.quiet:
            self.print(f"[bold red]❌ {message}[/bold red]")

    def success(self, message):
        if not self.quiet:
            self.print(f"[bold green]✅ {message}[/bold green]")

    def status(self, *args, **kwargs):
        if not self.quiet:
            return super().status(*args, **kwargs)
        else:
            return EmptyContextManager()


class EmptyContextManager:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

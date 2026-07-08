#!/usr/bin/env python3
"""
MovieForge CLI - Command Line Interface
Forge your movie collection from the terminal
"""

import os
import sys
import argparse
import subprocess

import requests
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel

console = Console()

DEFAULT_SERVER = "http://localhost:5000"


class MovieForgeCLI:
    def __init__(self, server_url=None):
        self.server_url = server_url or DEFAULT_SERVER
        self.session = requests.Session()

    def test_connection(self):
        try:
            response = self.session.get(f"{self.server_url}/api/movies", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def list_movies(self):
        try:
            response = self.session.get(f"{self.server_url}/api/movies")
            if response.status_code != 200:
                console.print("[red]❌ Failed to fetch movies[/red]")
                return

            movies = response.json()
            auth_response = self.session.get(f"{self.server_url}/api/auth")
            auth = auth_response.json() if auth_response.status_code == 200 else {}

            table = Table(title="🎬 Available Movies", style="cyan")
            table.add_column("🎥 Movie", style="bold magenta")
            table.add_column("🎭 Hero", style="green")
            table.add_column("👤 Username", style="yellow")
            table.add_column("🔑 Password", style="red")
            table.add_column("📊 Status", style="white")

            for username, movie in movies.items():
                status = "✅ Uploaded" if movie.get("uploaded") else "❌ Not Uploaded"
                password = auth.get(username, "Unknown")
                table.add_row(
                    movie.get("name", username),
                    movie.get("hero", "Unknown"),
                    username,
                    password,
                    status,
                )

            console.print(table)
        except Exception as exc:
            console.print(f"[red]❌ Error: {exc}[/red]")

    def upload_movie(self, username, file_path):
        if not os.path.exists(file_path):
            console.print(f"[red]❌ File not found: {file_path}[/red]")
            return

        size_gb = os.path.getsize(file_path) / (1024 * 1024 * 1024)
        console.print(f"[yellow]📤 Uploading: {os.path.basename(file_path)} ({size_gb:.2f} GB)[/yellow]")

        try:
            with open(file_path, "rb") as handle:
                files = {"movie": (os.path.basename(file_path), handle, "video/mp4")}
                with Progress(
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    TimeElapsedColumn(),
                    console=console,
                ) as progress:
                    task = progress.add_task("[cyan]Uploading...", total=100)
                    response = self.session.post(
                        f"{self.server_url}/upload/{username}",
                        files=files,
                        timeout=3600,
                    )
                    progress.update(task, completed=100)

            if response.status_code in [200, 302]:
                console.print("[green]✅ Upload successful![/green]")
                console.print(f"[cyan]🌐 Watch at: {self.server_url}/watch/{username}[/cyan]")
            else:
                console.print(f"[red]❌ Upload failed: {response.status_code}[/red]")
        except Exception as exc:
            console.print(f"[red]❌ Upload error: {exc}[/red]")

    def watch_movie(self, username):
        url = f"{self.server_url}/watch/{username}"
        console.print(f"[green]🎬 Opening: {url}[/green]")
        try:
            if sys.platform == "win32":
                os.startfile(url)
            elif sys.platform == "darwin":
                subprocess.run(["open", url])
            else:
                subprocess.run(["xdg-open", url])
        except Exception as exc:
            console.print(f"[red]❌ Could not open browser: {exc}[/red]")
            console.print(f"[yellow]📋 Copy this URL: {url}[/yellow]")

    def get_credentials(self, username=None):
        try:
            response = self.session.get(f"{self.server_url}/api/auth")
            if response.status_code != 200:
                console.print("[red]❌ Failed to fetch credentials[/red]")
                return

            auth = response.json()
            if username:
                if username in auth:
                    console.print(f"\n[bold green]🎥 Movie:[/bold green] {username}")
                    console.print(f"[bold yellow]🔑 Password:[/bold yellow] {auth[username]}")
                else:
                    console.print(f"[red]❌ Movie not found: {username}[/red]")
            else:
                table = Table(title="🔐 All Credentials", style="cyan")
                table.add_column("👤 Username", style="yellow")
                table.add_column("🔑 Password", style="red")
                for name, password in auth.items():
                    table.add_row(name, password)
                console.print(table)
        except Exception as exc:
            console.print(f"[red]❌ Error: {exc}[/red]")

    def server_info(self):
        try:
            response = self.session.get(f"{self.server_url}/api/url")
            if response.status_code != 200:
                console.print("[red]❌ Server unreachable[/red]")
                return
            data = response.json()
            console.print(
                Panel.fit(
                    f"[bold cyan]🎬 MovieForge Server[/bold cyan]\n"
                    f"[green]URL:[/green] {data.get('url', 'Unknown')}\n"
                    f"[green]Movies:[/green] {len(data.get('movies', {}))}\n"
                    f"[green]Status:[/green] ✅ Online",
                    title="Server Info",
                    border_style="cyan",
                )
            )
        except Exception as exc:
            console.print(f"[red]❌ Server unreachable: {exc}[/red]")

    def interactive_mode(self):
        console.print(
            Panel.fit(
                "[bold cyan]🎬 MovieForge Interactive CLI[/bold cyan]\n"
                "Forge your movie collection, watch anywhere",
                border_style="cyan",
            )
        )
        while True:
            console.print("\n[bold]Commands:[/bold]")
            console.print("  [cyan]1.[/cyan] List movies")
            console.print("  [cyan]2.[/cyan] Upload movie")
            console.print("  [cyan]3.[/cyan] Watch movie")
            console.print("  [cyan]4.[/cyan] Get credentials")
            console.print("  [cyan]5.[/cyan] Server info")
            console.print("  [cyan]6.[/cyan] Set server URL")
            console.print("  [cyan]0.[/cyan] Exit")
            choice = input("\n[bold]Select option:[/bold] ").strip()
            if choice == "0":
                console.print("[yellow]👋 Goodbye![/yellow]")
                break
            if choice == "1":
                self.list_movies()
            elif choice == "2":
                username = input("👤 Enter username: ").strip()
                file_path = input("📁 Enter file path: ").strip()
                self.upload_movie(username, file_path)
            elif choice == "3":
                username = input("👤 Enter username: ").strip()
                self.watch_movie(username)
            elif choice == "4":
                username = input("👤 Enter username (press Enter for all): ").strip()
                self.get_credentials(username if username else None)
            elif choice == "5":
                self.server_info()
            elif choice == "6":
                self.server_url = input("🌐 Enter server URL: ").strip()
                console.print("[green]✅ Server URL updated![/green]")
            else:
                console.print("[red]❌ Invalid option[/red]")


def main():
    parser = argparse.ArgumentParser(description="MovieForge CLI - Forge your movie collection, watch anywhere")
    parser.add_argument("--url", "-u", default=DEFAULT_SERVER, help=f"Server URL (default: {DEFAULT_SERVER})")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    subparsers.add_parser("list", help="List all movies")
    upload_parser = subparsers.add_parser("upload", help="Upload a movie")
    upload_parser.add_argument("username", help="Username (movie name)")
    upload_parser.add_argument("file", help="Path to movie file")
    watch_parser = subparsers.add_parser("watch", help="Watch a movie")
    watch_parser.add_argument("username", help="Username (movie name)")
    creds_parser = subparsers.add_parser("creds", help="Get credentials")
    creds_parser.add_argument("username", nargs="?", help="Username (optional)")
    subparsers.add_parser("info", help="Show server info")
    subparsers.add_parser("interactive", help="Interactive mode")

    args = parser.parse_args()
    cli = MovieForgeCLI(args.url)

    if not cli.test_connection():
        console.print("[red]❌ Cannot connect to server![/red]")
        console.print(f"[yellow]💡 Make sure the server is running at: {cli.server_url}[/yellow]")
        if args.command:
            return

    if args.command == "list":
        cli.list_movies()
    elif args.command == "upload":
        cli.upload_movie(args.username, args.file)
    elif args.command == "watch":
        cli.watch_movie(args.username)
    elif args.command == "creds":
        cli.get_credentials(args.username)
    elif args.command == "info":
        cli.server_info()
    elif args.command == "interactive":
        cli.interactive_mode()
    else:
        parser.print_help()
        console.print("\n[cyan]💡 Try: python cli.py interactive[/cyan]")


if __name__ == "__main__":
    main()

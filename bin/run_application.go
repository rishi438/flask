package main

import (
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"sync"
	"time"
)

func main() {
	backendDir := "./backend"
	if err := os.Chdir(backendDir); err != nil {
		log.Fatalf("Error changing working directory: %v", err)
	}
	activateScript := filepath.Join("venv", "Scripts", "Activate")
	cmd := exec.Command("powershell", "-Command", activateScript)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		log.Fatalf("Error activating virtual environment: %v", err)
	}

	var wg sync.WaitGroup

	commands := []string{
		"python run.py",
		"celery -A run.celery_scheduler worker --pool=solo -l info",
		"celery -A run.celery_scheduler beat -l info",
		"celery -A run.celery_scheduler flower",
	}

	for _, cmd := range commands {
		wg.Add(1)
		go func(cmd string) {
			defer wg.Done()
			runCommand(cmd)
			time.Sleep(500 * time.Millisecond) // Introduce a delay between commands
		}(cmd)
	}

	wg.Wait()
}

func runCommand(cmd string) {
	cmdExec := exec.Command("powershell", "-Command", cmd)
	cmdExec.Stdout = os.Stdout
	cmdExec.Stderr = os.Stderr
	if err := cmdExec.Run(); err != nil {
		log.Fatalf("Error running command %q: %v", cmd, err)
	}
}

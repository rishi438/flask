package main

import (
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"sync"
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

	commands := []func(){
		func() {
			defer wg.Done()
			log.Printf("Executing command: %s\n", "python run.py")
			runCommand("python run.py")
		},
		func() {
			defer wg.Done()
			log.Printf("Executing command: %s\n", "celery -A run.celery_scheduler worker --pool=solo -l info")
			runCommand("celery -A run.celery_scheduler worker --pool=solo -l info")
		},
		func() {
			defer wg.Done()
			log.Printf("Executing command: %s\n", "celery -A run.celery_scheduler beat -l info")
			runCommand("celery -A run.celery_scheduler beat -l info")
		},
		func() {
			defer wg.Done()
			log.Printf("Executing command: %s\n", "celery -A run.celery_scheduler flower")
			runCommandWithOutput("celery -A run.celery_scheduler flower")
		},
	}

	for _, cmd := range commands {
		wg.Add(1)
		go cmd()
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

func runCommandWithOutput(cmd string) {
	cmdExec := exec.Command("powershell", "-Command", cmd)
	output, err := cmdExec.CombinedOutput()
	if err != nil {
		log.Fatalf("Error running command %q: %v\nOutput:\n%s", cmd, err, output)
	}
	log.Printf("Command %q output:\n%s", cmd, output)
}

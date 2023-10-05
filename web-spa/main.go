package main

import (
	"encoding/json"
	"net/http"
)

type AdminResponse struct {
	IsAdmin bool `json:"isAdmin"`
}

func main() {
	fs := http.FileServer(http.Dir("./dist"))
	http.Handle("/", fs)

	http.HandleFunc("/api/isAdmin", func(w http.ResponseWriter, r *http.Request) {
		response := AdminResponse{
			IsAdmin: false,
		}

		jsonResponse, err := json.Marshal(response)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonResponse)
	})

	port := "8080"
	println("Server is running on port " + port)
	err := http.ListenAndServe(":"+port, nil)
	if err != nil {
		panic(err)
	}
}

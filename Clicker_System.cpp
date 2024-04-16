#include <iostream>
#include <fstream>
#include <thread>
#include <chrono>
#include <conio.h>
#include <Windows.h>
#include "json/single_include/nlohmann/json.hpp"


void autoclicker(float clicks_per_second, int mouse_button) {
    INPUT input = {0};


    if (mouse_button == 1) {
        while(true){
            input.type = INPUT_MOUSE;
            input.mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
            SendInput(1, &input, sizeof(INPUT));
            ZeroMemory(&input, sizeof(INPUT));
            input.type = INPUT_MOUSE;
            input.mi.dwFlags = MOUSEEVENTF_LEFTUP;
            SendInput(1, &input, sizeof(INPUT));
            ZeroMemory(&input, sizeof(INPUT));
            Sleep(clicks_per_second);
        }
    } else if (mouse_button == 2) {
        while(true){
            Sleep(clicks_per_second);
            input.type = INPUT_MOUSE;
            input.mi.dwFlags = MOUSEEVENTF_RIGHTDOWN;
            SendInput(1, &input, sizeof(INPUT));
            ZeroMemory(&input, sizeof(INPUT));
            input.type = INPUT_MOUSE;
            input.mi.dwFlags = MOUSEEVENTF_RIGHTUP;
            SendInput(1, &input, sizeof(INPUT));
            ZeroMemory(&input, sizeof(INPUT));
        }
    } else {
        std::cerr << "Invalid mouse button" << std::endl;
        return;
    }
}


int main() {
    std::ifstream file("settings.json");
    if (!file.is_open()) {
        std::cerr << "Failed to open settings file" << std::endl;
        return 1;
    }

    nlohmann::json root;
    file >> root;

    int clicks_per_second = root["click_interval"].get<int>();
    float mouse_button = root["mouse_button"].get<float>();

    autoclicker(clicks_per_second, mouse_button);
    return 0;
}
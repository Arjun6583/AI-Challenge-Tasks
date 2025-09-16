#include <iostream>
#include <windows.h>
#include <string>

#ifdef _WIN32
#define PATH_SEPARATOR '\\'
#else
#define PATH_SEPARATOR '/'
#endif

bool b_fileFound = false;

bool searchFile(const std::string& directory, const std::string& filename)
{
    std::string searchPath = directory + "\\*";

    WIN32_FIND_DATAA findFileData;
    HANDLE hFind = FindFirstFileA(searchPath.c_str(), &findFileData);

    if (hFind == INVALID_HANDLE_VALUE)
    {
        std::cerr << "Error opening directory: " << directory << std::endl;
        return false;
    }

    do
    {
        const char* name = findFileData.cFileName;

        if (strcmp(name, ".") == 0 || strcmp(name, "..") == 0)
            continue;

        std::string fullPath = directory + PATH_SEPARATOR + name;

        if (findFileData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
        {
            searchFile(fullPath, filename);
        }
        else if (!b_fileFound && filename == name)
        {
            b_fileFound = true;
            break;
        }

    } while (FindNextFileA(hFind, &findFileData) != 0);

    FindClose(hFind);
    return b_fileFound;
}

int main(int argc, char* argv[])
{
    if (argc != 3)
    {
        std::cerr << "Usage: <filename> <directory>" << std::endl;
        return EXIT_FAILURE;
    }

    const std::string fileName = argv[1];
    const std::string folderName = argv[2];

    bool found = searchFile(folderName, fileName);

    if (found == true)
    {
        std::cout << "File " << fileName << " found in " << folderName << std::endl;
        return EXIT_SUCCESS;
    }

    std::cout << "File " << fileName << " not found in " << folderName << std::endl;
    return EXIT_FAILURE;
    
}

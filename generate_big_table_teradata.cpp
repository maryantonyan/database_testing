#include <fstream>
#include <string>
#include <cstdlib>
#include <ctime> 
#include <iomanip>

std::string get_random_string(const int len) {
    char *s = new char[len + 1];
    static const char alphanum[] =
        "0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz";

    for (int i = 0; i < len; ++i) {
        s[i] = alphanum[rand() % (sizeof(alphanum) - 1)];
    }
    s[len] = 0;
    std::string result(s);
    delete[] s;
    return result;
}

std::string get_random_integer(const int len) {
    char *s = new char[len + 1];
    static const char alphanum[] = "123456789";

    for (int i = 0; i < len; ++i) {
        s[i] = alphanum[rand() % (sizeof(alphanum) - 1)];
    }
    s[len] = 0;
    std::string result(s);
    delete[] s;
    return result;
}

double get_random_double(double fMin, double fMax) {
    double f = (double)rand() / RAND_MAX;
    return fMin + f * (fMax - fMin);
}

int main() {
    std::string char_1;
    std::string smallint;
    std::string bigint;
    float real;
    double _double;
    std::string integer;
    std::string char_2;

    srand(time(NULL));
    std::ofstream file("./testing_table_big_teradata.csv");
    for (unsigned int serial = 0; serial <= 100000; ++serial) {
        char_1 = get_random_string(25);
        smallint = get_random_integer(4);
        bigint = get_random_integer(9);
        real =
            static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / 10));
        _double = get_random_double(0, 10);
        integer = get_random_integer(7);
        char_2 = get_random_string(25);

        std::string id = std::to_string(serial);
        unsigned int length = 5 - id.length();
        file << id;
        for (unsigned int j = 0; j < length; ++j) {
            file << " ";
        }
        file << "|" << char_1 << "|" << smallint << "|"
             << bigint << "|" << std::fixed << std::setprecision(6) << real << "|"
             << std::setprecision(15) << _double << "|"
             << integer << "|" << char_2 << "\n";
    }
    return 0;
}

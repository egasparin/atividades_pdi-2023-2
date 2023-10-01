#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

void funcaoMouse(int event, int x, int y, int flags, void *userdata)
{
    if (event == EVENT_LBUTTONDOWN)
        cout << "Botao esquerdo clicado - coordenada (" << x << ", " << y << ")" << endl;
    else if (event == EVENT_RBUTTONDOWN)
        cout << "Botao direito clicado - coordenada (" << x << ", " << y << ")" << endl;
    else if (event == EVENT_MBUTTONDOWN)
        cout << "Botao do meio clicado - coordenada (" << x << ", " << y << ")" << endl;
    else if (event == EVENT_MOUSEMOVE)
        cout << "Movimento do mouse - coordenada (" << x << ", " << y << ")" << endl;
}

void funcaoMouse2(int event, int x, int y, int flags, void *userdata)
{
    if (flags == (EVENT_FLAG_CTRLKEY + EVENT_FLAG_LBUTTON))
        cout << "Botão esquerdo e CTRL apertados - usuário (" << *(string *)userdata << ")" << endl;
    else if (flags == (EVENT_FLAG_RBUTTON + EVENT_FLAG_SHIFTKEY))
        cout << "Botão direito e SHIFT apertados - usuário (" << *(string *)userdata << ")" << endl;
    else if (event == EVENT_MOUSEMOVE && flags == EVENT_FLAG_ALTKEY)
        cout << "Mouse movimentado e ALT apertado - usuário (" << *(string *)userdata << ")" << endl;
}

int main()
{
    Mat img = imread("./Imagens/futurama.jpg");

    string name = "Eduardo";

    namedWindow("Original", WINDOW_NORMAL);
    setMouseCallback("Original", funcaoMouse2, &name);
    imshow("Original", img);
    waitKey(0);
    return 0;
}
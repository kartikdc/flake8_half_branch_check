def main():
    if 2 == 2:
        print("True")
    else:
        print("False")

    if True:
        if True:
            pass

    def a():
        if 1 == 2:
            pass
        elif 2 == 2:
            print("True")

    if 3 == 2:
        print("Don't print!")


if __name__ == "__main__":
    main()

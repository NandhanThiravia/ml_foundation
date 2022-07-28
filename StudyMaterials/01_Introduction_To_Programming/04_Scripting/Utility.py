def mean(num_list):
    return (sum(num_list) / len(num_list))

def main():
    num_list = [547, 5478, 384, 4854, 3847]
    print("Mean is: {}".format(mean(num_list)))
    
if __name__ == "__main__":
    main()
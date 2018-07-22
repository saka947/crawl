
#url='https://www.toutiao.com/search_content/?offset=19&format=json&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE&autoload=true&count=20&cur_tab=3&from=search_tab'
#get这个url返回一个json，关键的值是data，data里面是当前页面的文章主体，一个data[i]对象里有
#title，article_url两个比较关键的值
# offset是偏移量，0是从0偏移出count数量的文章，20就是从20-40
# en_wikipedia_toolkit
This is a toolkit for Wikipedia editors who wish to edit their pages easily.
这个套件是写给那些想更快编写维基百科的人用的。

**Now can only be used in English wikipedia.**
**目前只能用于英文维基百科。**

Then how to use the toolkit?
那么怎么用这个套件呢？

## Guideline 指南
1. Fetch the source code of a page. 获取一个页面的源代码。
```
en_wikipedia_toolkit.en_wikipedia_toolkit().fetch_code(page)
```
For example, if one want to fetch the code of the page "Taylor Swift" (an American singer) (with the article pic shown in Fig. 1 and Fig. 2), just run this code:

举个例子，如果一个人想获取"Taylor Swift"（一位美国女歌手）条目（图1和图2分别显示了条目和源代码）的源代码，只需运行这段代码：
```
en_wikipedia_toolkit.en_wikipedia_toolkit().fetch_code("Taylor Swift")
```
Then the output will go like this:

那么会输出：
```
Done. The source code was written in 'Taylor Swift.wikitext'.
All processes were done in xxx second(s).
```
And the source code has already been stored in your workspace.
源代码已经存储在你的工作区中了。


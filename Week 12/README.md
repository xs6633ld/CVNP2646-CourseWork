One of the prompts I used in ChatGPT with the oriningal script was to break down the script so I could undertsand it more and make suggestions on how I could improve this script to catch up with todays Python Language. The output deeply described the script and made me undertsand it a lot better. It also provided me many suggestions on how I could improve the script which I thought was super helpful and I incorporated them into my new script. I also had ChatGPT create the traffic sample log with a good variety of different traffic that I was able ot test with my script.


The original script had many issues with it as it was outdated. It used magic numbers which has been replaced and should not be used anymore. It also had no error handeling which could cause the script to crash. Many improvements to this script had to be made. 

I broke the script up into different sections to make a separtion of concerns. This made the script was easier to undertsand and follow and is also a best practice. It is super imortant to sperate your functions. I also created an effective log and json file after running the script which showed efficient details of the accomplishments of the script. 

To ensure I didn.t break functionality, I built a pytest which tests for every major function. This uses cases such as empty input datasets and invalid packet formats. It is always very important to test your script because you use it in a real case.

The most challening part about refactoring was separting functions. The original script was very messy so I took the apprach to do nearly a complete rebuild of the script providing the same function. This was a lot of work but was very efiicent in making the script up to date with todays python language. 

With separting functions, maintaince to the script has become much more easy. Having functions complete one tasks makes your script a lot more easy to follow and a lot more structured. This script is also now able to be tested which also improves maintainability.
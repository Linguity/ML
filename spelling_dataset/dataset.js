function myfunction() {
 /* This is a function to automate generating speech in https://ttsmp3.com/.
 the indexOption variable contains the english speaker option index. Delete the last file because it double at the end*/
   var indexOption = [1, 2, 6, 7, 8, 26, 27, 47, 48, 49, 50, 51, 52, 53, 54, 59];
  let i = 0;
  let interval = setInterval(() => {
    const delay = (delayInms) => {
      return new Promise((resolve) => setTimeout(resolve, delayInms));
    };

    const sample = async () => {
      document.getElementById("sprachwahl").options[indexOption[i]].selected =
        "selected";

      console.log("waiting...");
      let delayres = await delay(3000);
      document.getElementById("vorlesenbutton").click();
      document.getElementById("downloadenbutton").click();
      i++;
      if (i == indexOption.length) {
        clearInterval(interval);
      }
    };

    sample();
  }, 3000);
}



# changes

The big change v2.2.1 was the last release supporting libdataset. Moving forward there are two options.
You can either wrap the cli provided with Dataset >= v2.2.2 or you can wrap the JSON API web service provided by datasetd. The later approach has been used successfully with [ts_dataset](https://github.com/caltechlibrary/ts_dataset) which made Dataset available to TypeScript/Deno programs. This approach does require you to configure an run datasetd.


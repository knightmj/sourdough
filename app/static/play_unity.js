
function UnityGameLoaded() {
    unityInstance.SendMessage("Board", "SetName", $("#player").val())
    unityInstance.SendMessage("Board", "SetHost", "http://" +  window.location.hostname)

    unityInstance.SendMessage("Board", "StartGame", $("#game_name").val())
}

var settings =
{
     onProgress: UnityProgress,
     Module:
     {
         preRun: [ function() { console.log("About to run....") ; } ],
         postRun: [ function() {
         } ],
     }
 };

var unityInstance = UnityLoader.instantiate("unityContainer", "/static/Build/test.json", settings);
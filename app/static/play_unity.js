function startGame(){
    unityInstance.SendMessage("Board", "SetName", $("#player").val())
    unityInstance.SendMessage("Board", "StartGame", $("#game_name").val())

}
var settings =
{
     onProgress: UnityProgress,
     Module:
     {
         preRun: [ function() { console.log("About to run....") ; } ],
         postRun: [ function() {
            // hack until we we have a method that says we can start the game.
            setTimeout(startGame, 4000)
         } ],
     }
 };

var unityInstance = UnityLoader.instantiate("unityContainer", "/static/Build/test.json", settings);
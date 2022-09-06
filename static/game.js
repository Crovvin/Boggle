class Game{
    
    constructor(boardId, seconds = 60) {
        this.seconds = seconds;
        this.postTimer();
        this.board = $("#" + boardId);
        this.score = 0;
        this.words = new Set();
        this.timer = setInterval(this.tick.bind(this), 1000);
        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
      }

      postMessage(message, cls) {
        $(".message", this.board)
          .text(message)
          .removeClass()
          .addClass(`message ${cls}`);
      }
    
      postWord(word) {
        $(".words", this.board).append($("<li>", { text: word }));
      }
    
      postScore() {
        $(".score", this.board).text(this.score);
      }
    
      async handleSubmit(e) {
        e.preventDefault();
        const $word = $(".word", this.board);
        let word = $word.val();
        if (!word) return;
        if (this.words.has(word)) {
          this.postMessage(`Already found ${word}`, "error");
          return;
        }
        const resp = await axios.get("/checkforword", { params: { word: word }});
        if (resp.data.result === "notaword") {
          this.postMessage(`${word} is not an English word`, "error");
        } else if (resp.data.result === "notontheboard") {
          this.postMessage(`${word} is not a word on the board`, "error");
        } else {
          this.postWord(word);
          this.score += word.length;
          this.postScore();
          this.words.add(word);
          this.postMessage(`Added: ${word}`, "yes");
        }
    
        $word.val("").focus();
      }
    
      postTimer() {
        $(".timer", this.board).text(this.seconds);
      }
    
      async tick() {
        this.seconds = this.seconds - 1;
        this.postTimer();
        if (this.seconds === 0) {
          clearInterval(this.timer);
          await this.scoreGame();
        }
      }
    
      async scoreGame() {
        $(".add-word", this.board).hide();
        const resp = await axios.post("/post-score", { score: this.score });
        if (resp.data.brokeRecord) {
          this.postMessage(`New record! : ${this.score}`, "yes");
        } else {
          this.postMessage(`Final score! : ${this.score}`, "yes");
        }
      }
    }
    
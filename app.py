# -<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini Geometry Dash</title>
    <style>
        body {
            margin: 0;
            background-color: #1a1a1a;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            font-family: Arial, sans-serif;
        }
        canvas {
            border: 4px solid #fff;
            background-color: #222;
        }
        #score {
            position: absolute;
            top: 20px;
            color: white;
            font-size: 24px;
        }
    </style>
</head>
<body>

<div id="score">Score: 0</div>
<canvas id="gameCanvas" width="800" height="400"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const scoreElement = document.getElementById("score");

// 게임 상태
let score = 0;
let isGameOver = false;

// 플레이어 (사각형)
const player = {
    x: 100,
    y: 300,
    size: 40,
    color: #00ffff,
    gravity: 0.6,
    jumpForce: -12,
    velocityY: 0,
    isGrounded: false,
    rotation: 0
};

// 장애물 (삼각형) 배열
const obstacles = [];
let obstacleTimer = 0;

// 바닥 높이
const groundY = 340;

// 키 입력 감지
window.addEventListener("keydown", (e) => {
    if ((e.code === "Space" || e.code === "ArrowUp")) {
        if (player.isGrounded && !isGameOver) {
            player.velocityY = player.jumpForce;
            player.isGrounded = false;
        } else if (isGameOver) {
            resetGame();
        }
    }
});

// 터치/클릭 입력 감지 (모바일용)
window.addEventListener("click", () => {
    if (player.isGrounded && !isGameOver) {
        player.velocityY = player.jumpForce;
        player.isGrounded = false;
    } else if (isGameOver) {
        resetGame();
    }
});

function spawnObstacle() {
    obstacleTimer++;
    // 무작위 주기로 장애물 생성
    if (obstacleTimer > Math.random() * 60 + 90) {
        obstacles.push({
            x: canvas.width,
            y: groundY,
            size: 40,
            speed: 6 + score * 0.2 // 점수가 높을수록 빨라짐
        });
        obstacleTimer = 0;
    }
}

function update() {
    if (isGameOver) return;

    // 플레이어 중력 및 물리 적용
    player.velocityY += player.gravity;
    player.y += player.velocityY;

    // 바닥 착지 충돌 처리
    if (player.y + player.size >= groundY) {
        player.y = groundY - player.size;
        player.velocityY = 0;
        player.isGrounded = true;
    }

    // 공중에 있을 때 회전 애니메이션 (지오메트리 대시 감성)
    if (!player.isGrounded) {
        player.rotation += 0.1;
    } else {
        // 바닥에 있으면 각도 정렬
        player.rotation = Math.round(player.rotation / (Math.PI / 2)) * (Math.PI / 2);
    }

    // 장애물 업데이트
    spawnObstacle();
    for (let i = obstacles.length - 1; i >= 0; i--) {
        const obs = obstacles[i];
        obs.x -= obs.speed;

        // 화면 밖으로 나간 장애물 제거 및 점수 획득
        if (obs.x + obs.size < 0) {
            obstacles.splice(i, 1);
            score++;
            scoreElement.innerText = "Score: " + score;
            continue;
        }

        // 충돌 체크 (간단한 AABB 및 점 충돌 근사화)
        if (
            player.x < obs.x + obs.size &&
            player.x + player.size > obs.x &&
            player.y + player.size > obs.y - obs.size
        ) {
            isGameOver = true;
        }
    }
}

function draw() {
    // 화면 비우기
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 바닥 그리기
    ctx.fillStyle = "#333";
    ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, groundY);
    ctx.lineTo(canvas.width, groundY);
    ctx.stroke();

    // 플레이어 그리기 (회전 적용)
    ctx.save();
    ctx.translate(player.x + player.size / 2, player.y + player.size / 2);
    ctx.rotate(player.rotation);
    ctx.fillStyle = player.color;
    ctx.fillRect(-player.size / 2, -player.size / 2, player.size, player.size);
    ctx.strokeStyle = "#fff";
    ctx.strokeRect(-player.size / 2, -player.size / 2, player.size, player.size);
    ctx.restore();

    // 장애물 그리기 (삼각형)
    ctx.fillStyle = "#ff4757";
    obstacles.forEach(obs => {
        ctx.beginPath();
        ctx.moveTo(obs.x, obs.y);
        ctx.lineTo(obs.x + obs.size / 2, obs.y - obs.size);
        ctx.lineTo(obs.x + obs.size, obs.y);
        ctx.closePath();
        ctx.fill();
        ctx.strokeStyle = "#fff";
        ctx.stroke();
    });

    // 게임 오버 메시지
    if (isGameOver) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "#fff";
        ctx.font = "40px Arial";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2);
        ctx.font = "20px Arial";
        ctx.fillText("Press Space or Click to Restart", canvas.width / 2, canvas.height / 2 + 40);
    }
}

function resetGame() {
    obstacles.length = 0;
    score = 0;
    scoreElement.innerText = "Score: " + score;
    player.y = groundY - player.size;
    player.velocityY = 0;
    player.isGrounded = true;
    player.rotation = 0;
    isGameOver = false;
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

// 게임 시작
gameLoop();
</script>

</body>
</html>
